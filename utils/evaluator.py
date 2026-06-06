import re
from utils.skill_extractor import SKILL_DICTIONARY, extract_skills
from utils.matcher import calculate_ats_score
from utils.preprocess import clean_text

def simulate_job_fit(resume_text, found_skills):
    """
    Tests the resume against every role in the dictionary to find high-potential matches.
    Returns sorted list of {role, score, match_type}
    """
    cleaned_resume = clean_text(resume_text)
    fit_results = []
    
    for role, expected_skills in SKILL_DICTIONARY.items():
        # Calculate a quick overlap score
        matching = [s for s in expected_skills if s in found_skills]
        overlap_score = (len(matching) / len(expected_skills)) * 100
        
        # Calculate semantic similarity
        jd_proxy = " ".join(expected_skills)
        semantic_score = calculate_ats_score(cleaned_resume, clean_text(jd_proxy))
        
        # Blended fit score
        fit_score = round((overlap_score * 0.4) + (semantic_score * 0.6), 1)
        
        if fit_score > 30: # Only report credible matches
            fit_results.append({
                "role": role,
                "score": fit_score,
                "match_type": "High" if fit_score > 75 else "Moderate" if fit_score > 50 else "Potential"
            })
            
    # Sort by score descending
    return sorted(fit_results, key=lambda x: x['score'], reverse=True)[:5]

def get_recruiter_insights(resume_text, found_skills, missing_skills):
    """
    Identifies "Attention Zones" and "Critical Friction Points" for humans.
    """
    insights = []
    text_lower = resume_text.lower()
    
    # 1. Formatting & Impact
    if "%" not in resume_text and not any(char.isdigit() for char in resume_text):
        insights.append({"type": "warning", "text": "Low Quantifiable Data: Recruiters look for metrics. Your profile lacks numerical proof of impact."})
    
    # 2. Skill Concentration
    if len(found_skills) > 12:
        insights.append({"type": "success", "text": "High Technical Density: Your keyword saturation will trigger top-tier ATS filters."})
    elif len(found_skills) < 5:
        insights.append({"type": "danger", "text": "Skill Scarcity: The document feels 'thin' to automated scanners. Inject more domain-specific nouns."})
        
    return insights

def extract_highlight_spans(resume_text, keywords):
    """
    Returns indices of keyword occurrences for UI highlighting (Heatmap).
    """
    spans = []
    text_lower = resume_text.lower()
    for kw in keywords:
        # Avoid very short words to reduce noise
        if len(kw) < 3: continue
        
        for m in re.finditer(r'\b' + re.escape(kw) + r'\b', text_lower):
            spans.append({"start": m.start(), "end": m.end(), "text": kw})
    return spans
