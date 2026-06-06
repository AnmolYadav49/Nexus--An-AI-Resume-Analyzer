# Connect React Frontend to Flask Analysis Pipeline

Standardize the resume upload and analysis flow through a single, production-ready REST API endpoint `/api/analyze`. This ensures that when the user uploads a PDF or DOCX file, the backend parses it, runs classification, extracts skills, calculates ATS similarity and Resume DNA metrics, and returns a unified JSON response. The React frontend will consume this response and display the actual analysis results.

---

## User Review Required

> [!IMPORTANT]
> **API Deprecations & Frontend Fallback Removal**
> * The existing `/api/generate_resume` endpoint (which returns mock/heuristic evaluations) will be deprecated.
> * The React frontend's fallback logic to the offline FastAPI microservice will be removed. All requests will go directly to Flask.
> * We will create a missing [config.js](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/frontend/src/config.js) in the frontend project to declare the API base paths properly.

> [!WARNING]
> **No UI Redesign Commitment**
> * The user interface layout, typography, and theme will remain unchanged as requested. The changes are strictly backend data binding and frontend React state/props mappings.

---

## Open Questions

> [!NOTE]
> **None**
> * All requirements (JSON schema, modules to connect, and constraints) are fully specified by the user.

---

## Proposed Changes

### Backend (Python/Flask)

#### [MODIFY] [app.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/app.py)
* Register a new route `POST /api/analyze` supporting file upload via `multipart/form-data`.
* Process flow:
  1. Extract the uploaded file (PDF/DOCX) from `request.files['resume']`.
  2. Save the file temporarily, pass the path to `extract_text` ([parser.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/parser.py)), and clean the file immediately.
  3. Clean text using `clean_text` ([preprocess.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/preprocess.py)).
  4. Run ML model classifier/vectorizer to get `predicted_role` and `confidence` percentage.
  5. Run skill extraction via `extract_skills` and `get_missing_skills` ([skill_extractor.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/skill_extractor.py)).
  6. Calculate ATS score using `calculate_ats_score` ([matcher.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/matcher.py)) comparing the cleaned resume text to expected skills.
  7. Compute Resume DNA metrics using `calculate_dna_matrix` ([matcher.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/matcher.py)).
  8. Generate suggestions using `generate_suggestions` ([suggestions.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/suggestions.py)).
  9. Extract experience bullets from the resume text and run them through `enhance_bullet` ([ai_generator.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/ai_generator.py)).
  10. Return a JSON response adhering exactly to the designed schema.

#### [MODIFY] [ai_generator.py](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/utils/ai_generator.py)
* Add a utility function `extract_experience_lines(raw_text)` that parses lines from raw resume text (filtering by line length and presence of typical action words or bullet prefixes) to find passive bullets.
* Enhance these bullets using the existing `enhance_bullet` function and return a list of up to 4 enhanced bullets.

---

### Frontend (React/Vite)

#### [NEW] [config.js](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/frontend/src/config.js)
* Expose baseline environment configurations:
  ```javascript
  export const FLASK_BASE = 'http://127.0.0.1:5000';
  export const FASTAPI_BASE = 'http://127.0.0.1:8000';
  ```

#### [MODIFY] [App.jsx](file:///c:/Users/Anmol%20Yadav/Desktop/ai-resume-builder/frontend/src/App.jsx)
* **File Upload**: Update `handleAnalyze` to build a `FormData` object, append the binary file under key `resume`, and POST to `${FLASK_BASE}/api/analyze`.
* **State Management**: Update states and results to match the new backend schema format.
* **Result Rendering**: Update `ResultPanel` data-bindings:
  * Display `predicted_role` and `confidence` prominently.
  * Display `ats_score` as a match metric.
  * Render `matched_skills` and `missing_skills` inline as badge pills.
  * Render `suggestions` in the suggestions container.
  * Render the `enhanced_bullets` in the enhanced experience section.

---

## Verification Plan

### Automated Tests
* We will verify the Flask server compiles and starts without errors:
  ```powershell
  python app.py
  ```
* Run existing backend tests:
  ```powershell
  python test_api.py
  ```

### Manual Verification
1. Start the Flask backend server on `http://127.0.0.1:5000`.
2. Start the Vite React development server:
   ```powershell
   npm run dev --prefix frontend
   ```
3. Open the browser, drag-and-drop a PDF resume, and click "Enhance with AI".
4. Verify the analysis runs, extracts the actual text, and displays the predicted role, ATS score, dynamic suggestions, and rewritten active bullets.
