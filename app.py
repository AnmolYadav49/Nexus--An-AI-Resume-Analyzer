from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import joblib
from datetime import datetime

# Load environment variables first
load_dotenv()

# Corrected Imports from structurally modular parts
from utils.parser import extract_text
from utils.preprocess import clean_text
from utils.skill_extractor import extract_skills, get_missing_skills, SKILL_DICTIONARY
from utils.matcher import calculate_ats_score, calculate_resume_strength, calculate_dna_matrix, calculate_detailed_breakdown
from utils.suggestions import generate_suggestions
from utils.evaluator import simulate_job_fit, get_recruiter_insights, extract_highlight_spans

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'nexus-dev-fallback-key-change-in-prod')

# CORS Configuration
raw_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
ALLOWED_ORIGINS = [origin.strip() for origin in raw_origins.split(',') if origin.strip()]

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin:
        cleaned_origin = origin.lower().rstrip('/')
        cleaned_allowed = [o.lower().rstrip('/') for o in ALLOWED_ORIGINS]
        if cleaned_origin in cleaned_allowed or '*' in ALLOWED_ORIGINS:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response


@app.before_request
def handle_options_preflight():
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200




# Configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'.pdf', '.docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load ML Models — captured at startup
base_dir = os.path.dirname(os.path.abspath(__file__))
models_loaded = False
classifier = None
vectorizer = None
label_encoder = None

try:
    classifier = joblib.load(os.path.join(base_dir, 'model', 'model.pkl'))
    vectorizer = joblib.load(os.path.join(base_dir, 'model', 'tfidf.pkl'))
    label_encoder = joblib.load(os.path.join(base_dir, 'model', 'label_encoder.pkl'))
    models_loaded = True
    print("[OK] Nexus ML Models loaded successfully.")
except Exception as e:
    print(f"[ERROR] Error loading models: {e}")

# Pipeline module health — checked at startup
pipeline_status = {}
try:
    from utils.parser import extract_text as _et; pipeline_status['parser'] = True
except: pipeline_status['parser'] = False
try:
    from utils.preprocess import clean_text as _ct; pipeline_status['preprocess'] = True
except: pipeline_status['preprocess'] = False
try:
    from utils.skill_extractor import extract_skills as _es; pipeline_status['skill_extractor'] = True
except: pipeline_status['skill_extractor'] = False
try:
    from utils.matcher import calculate_ats_score as _ca; pipeline_status['matcher'] = True
except: pipeline_status['matcher'] = False
try:
    from utils.suggestions import generate_suggestions as _gs; pipeline_status['suggestions'] = True
except: pipeline_status['suggestions'] = False
try:
    from utils.evaluator import simulate_job_fit as _sjf; pipeline_status['evaluator'] = True
except: pipeline_status['evaluator'] = False
try:
    from utils.ai_generator import heuristic_resume_build as _hrb; pipeline_status['ai_generator'] = True
except: pipeline_status['ai_generator'] = False


def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


# ─────────────────────────────────────────────
# HEALTH CHECK ROUTES
# ─────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def api_health():
    """Basic server health check."""
    return jsonify({
        "status": "ok",
        "server": "flask",
        "version": "2.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "models_loaded": models_loaded
    })


@app.route('/api/model-status', methods=['GET'])
def api_model_status():
    """Reports ML model load status for each component."""
    return jsonify({
        "status": "ok" if models_loaded else "degraded",
        "models": {
            "classifier": models_loaded,
            "vectorizer": models_loaded,
            "label_encoder": models_loaded,
        },
        "supported_roles": list(label_encoder.classes_) if models_loaded else [],
        "role_count": len(label_encoder.classes_) if models_loaded else 0
    })


@app.route('/api/pipeline-status', methods=['GET'])
def api_pipeline_status():
    """Reports individual utility module load status."""
    all_ok = all(pipeline_status.values())
    return jsonify({
        "status": "ok" if all_ok else "degraded",
        "modules": pipeline_status,
        "models_loaded": models_loaded
    })



# ─────────────────────────────────────────────
# CORE API ANALYSIS ROUTE (JSON SCHEMA)
# ─────────────────────────────────────────────

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def api_analyze():
    # Handle preflight options request
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
        
    try:
        if 'resume' not in request.files:
            return jsonify({"success": False, "error": "No resume file provided"}), 400
            
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"success": False, "error": "Empty filename"}), 400
            
        job_description = request.form.get('job_description', '').strip()
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            try:
                # 1. Text Extraction
                ext = os.path.splitext(filename)[1].lower()
                raw_text = extract_text(file_path, ext)
                if not raw_text or len(raw_text.strip()) < 20:
                    return jsonify({"success": False, "error": "Could not extract text from document"}), 400
                    
                cleaned_text = clean_text(raw_text)
                
                # 2. Role Classification
                predicted_role = "Unknown"
                confidence = 0.0
                if models_loaded:
                    try:
                        X_vec = vectorizer.transform([cleaned_text])
                        probs = classifier.predict_proba(X_vec)[0]
                        pred_idx = classifier.predict(X_vec)[0]
                        predicted_role = label_encoder.inverse_transform([pred_idx])[0]
                        confidence = round(float(max(probs)) * 100, 2)
                    except Exception as e:
                        print(f"Classification failure: {e}")
                
                # 3. Skill Extraction
                found_skills = extract_skills(raw_text, predicted_role, job_description if job_description else None)
                missing_skills = get_missing_skills(found_skills, predicted_role, job_description if job_description else None)
                
                # 4. ATS Scoring
                jd_for_scoring = job_description
                if not jd_for_scoring:
                    expected = SKILL_DICTIONARY.get(predicted_role, [])
                    jd_for_scoring = " ".join(expected)
                    
                match_score = calculate_ats_score(cleaned_text, clean_text(jd_for_scoring))
                
                # 5. Suggestions
                suggestions = generate_suggestions(found_skills, missing_skills, match_score, predicted_role, raw_text)
                
                # 6. Resume DNA
                dna_matrix = calculate_dna_matrix(raw_text, found_skills)
                resume_dna = {
                    "technical": dna_matrix[0],
                    "leadership": dna_matrix[1],
                    "impact": dna_matrix[2],
                    "communication": dna_matrix[3],
                    "problem_solving": dna_matrix[4]
                }
                
                # 7. Enhanced experience bullets
                from utils.ai_generator import extract_experience_lines
                enhanced_bullets = extract_experience_lines(raw_text)
                
                return jsonify({
                    "success": True,
                    "predicted_role": predicted_role,
                    "confidence": confidence,
                    "ats_score": match_score,
                    "matched_skills": found_skills,
                    "missing_skills": missing_skills,
                    "resume_dna": resume_dna,
                    "suggestions": suggestions,
                    "enhanced_bullets": enhanced_bullets
                })
                
            finally:
                # Cleanup file
                try:
                    os.remove(file_path)
                except Exception:
                    pass
        else:
            return jsonify({"success": False, "error": "Allowed file types are PDF or DOCX only"}), 400
            
    except Exception as e:
        print(f"API analyze route error: {e}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


# ─────────────────────────────────────────────
# PAGE ROUTES
# ─────────────────────────────────────────────


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/how-it-works', methods=['GET'])
def how_it_works():
    return render_template('how_it_works.html')


@app.route('/auth', methods=['GET'])
def auth():
    return render_template('auth.html')


@app.route('/builder', methods=['GET'])
def builder():
    return render_template('builder.html')


@app.route('/preview', methods=['GET'])
def preview():
    return render_template('preview.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


# ─────────────────────────────────────────────
# CORE ANALYSIS ROUTE
# ─────────────────────────────────────────────

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'resume' not in request.files:
            flash('No physical artifact uploaded for analysis.')
            return redirect(url_for('index'))

        file = request.files['resume']
        if file.filename == '':
            flash('No selected document. Please drop a valid file.')
            return redirect(url_for('index'))

        job_description = request.form.get('job_description', '').strip()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # 1. Text Extraction
                ext = os.path.splitext(filename)[1].lower()
                raw_text = extract_text(file_path, ext)
                if not raw_text or len(raw_text.strip()) < 20:
                    flash('Could not extract meaningful text from this document. Try a different file.')
                    return redirect(url_for('index'))

                cleaned_text = clean_text(raw_text)

                # 2. Role Classification
                predicted_role = "Unknown"
                confidence = 0.0
                top_roles = []

                if models_loaded:
                    try:
                        X_vec = vectorizer.transform([cleaned_text])
                        probs = classifier.predict_proba(X_vec)[0]
                        pred_idx = classifier.predict(X_vec)[0]
                        predicted_role = label_encoder.inverse_transform([pred_idx])[0]
                        confidence = round(float(max(probs)) * 100, 2)
                        classes = label_encoder.classes_
                        top_indices = probs.argsort()[-3:][::-1]
                        top_roles = [{"role": classes[i], "prob": round(float(probs[i]) * 100, 1)} for i in top_indices]
                    except Exception as e:
                        print(f"Prediction pipeline failure: {e}")

                # 3. Skill Extraction
                found_skills = extract_skills(raw_text, predicted_role, job_description if job_description else None)
                missing_skills = get_missing_skills(found_skills, predicted_role, job_description if job_description else None)

                # 4. ATS Scoring — fallback to role baseline if no JD
                jd_for_scoring = job_description
                if not jd_for_scoring:
                    expected = SKILL_DICTIONARY.get(predicted_role, [])
                    jd_for_scoring = " ".join(expected)

                match_score = calculate_ats_score(cleaned_text, clean_text(jd_for_scoring))
                resume_strength = calculate_resume_strength(found_skills, missing_skills, match_score, cleaned_text)

                # 5. Suggestions
                suggestions = generate_suggestions(found_skills, missing_skills, match_score, predicted_role, raw_text)

                # 6. Advanced Analytics
                dna_matrix = calculate_dna_matrix(raw_text, found_skills)
                breakdown = calculate_detailed_breakdown(match_score, resume_strength, found_skills, missing_skills, raw_text)

                # 7. Elite Simulations
                job_fit = simulate_job_fit(raw_text, found_skills)
                recruiter_insights = get_recruiter_insights(raw_text, found_skills, missing_skills)
                highlights = extract_highlight_spans(raw_text, found_skills)

            finally:
                # Always clean up uploaded file
                try:
                    os.remove(file_path)
                except Exception:
                    pass

            return render_template('result.html',
                                   role=predicted_role,
                                   confidence=confidence,
                                   score=match_score,
                                   found_skills=found_skills,
                                   missing_skills=missing_skills,
                                   suggestions=suggestions,
                                   top_roles=top_roles,
                                   resume_strength=resume_strength,
                                   dna_matrix=dna_matrix,
                                   breakdown=breakdown,
                                   job_fit=job_fit,
                                   recruiter_insights=recruiter_insights,
                                   highlights=highlights,
                                   raw_text=raw_text)
        else:
            flash('Allowed file types are PDF or DOCX only.')
            return redirect(url_for('index'))

    except Exception as e:
        print(f"Analysis route error: {e}")
        flash('An unexpected error occurred during analysis. Please try again.')
        return redirect(url_for('index'))


# ─────────────────────────────────────────────
# API — SIMULATE (FIXED: NameError resolved)
# ─────────────────────────────────────────────

@app.route('/api/simulate', methods=['POST'])
def simulate():
    """
    Simulate resume analysis against a given role.
    Accepts JSON: { "role": "Python Developer", "raw_text": "..." }
    Returns structured JSON with all analysis fields.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        role = data.get('role', '').strip()
        raw_text = data.get('raw_text', '').strip()

        if not role:
            return jsonify({"error": "Missing required field: role"}), 400
        if not raw_text:
            return jsonify({"error": "Missing required field: raw_text"}), 400

        cleaned_text = clean_text(raw_text)

        # FIX: Define job_description BEFORE using it — build from role dictionary
        expected_skills = SKILL_DICTIONARY.get(role, [])
        if not expected_skills:
            # Role not in dictionary — use empty but don't crash
            job_description = ""
        else:
            job_description = " ".join(expected_skills)

        # 1. Skill Extraction — now job_description is always defined
        found_skills = extract_skills(raw_text, role, job_description if job_description else None)
        missing_skills = get_missing_skills(found_skills, role, job_description if job_description else None)

        # 2. ATS Scoring
        match_score = calculate_ats_score(cleaned_text, clean_text(job_description)) if job_description else 0.0
        resume_strength = calculate_resume_strength(found_skills, missing_skills, match_score, cleaned_text)

        # 3. Advanced Analytics
        dna_matrix = calculate_dna_matrix(raw_text, found_skills)
        breakdown = calculate_detailed_breakdown(match_score, resume_strength, found_skills, missing_skills, raw_text)
        suggestions = generate_suggestions(found_skills, missing_skills, match_score, role, raw_text)

        # 4. Simulations
        job_fit = simulate_job_fit(raw_text, found_skills)
        recruiter_insights = get_recruiter_insights(raw_text, found_skills, missing_skills)
        highlights = extract_highlight_spans(raw_text, found_skills)

        return jsonify({
            "role": role,
            "score": match_score,
            "resume_strength": resume_strength,
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "dna_matrix": dna_matrix,
            "breakdown": breakdown,
            "job_fit": job_fit,
            "recruiter_insights": recruiter_insights,
            "highlights": highlights
        })

    except Exception as e:
        print(f"Simulate route error: {e}")
        return jsonify({"error": "Internal analysis error. Please try again."}), 500


# ─────────────────────────────────────────────
# API — GENERATE RESUME (LEGACY / DEPRECATED)
# ─────────────────────────────────────────────

@app.route('/api/generate_resume', methods=['POST'])
def generate_resume():
    """
    [DEPRECATED] Heuristic resume builder — transforms passive text into impact-driven bullets.
    Legacy endpoint bypassed by the primary /api/analyze flow.
    Accepts JSON structured resume data, returns enhanced version.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        from utils.ai_generator import heuristic_resume_build
        resume_json = heuristic_resume_build(data)
        return jsonify(resume_json)

    except Exception as e:
        print(f"Generate resume error: {e}")
        return jsonify({"error": "Resume generation failed. Please try again."}), 500


if __name__ == '__main__':
    app.run(debug=True)
