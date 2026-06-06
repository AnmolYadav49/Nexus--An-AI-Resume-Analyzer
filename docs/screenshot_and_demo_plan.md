# Nexus AI Resume Builder: Screenshot & Demo Video Showcase Plan

This package provides a comprehensive plan for showcasing the **Nexus AI Resume Builder** on GitHub, LinkedIn, and portfolios.

---

## 1. Screenshot Capture Plan & Checklist

To capture professional screenshots showing authentic, realistic metrics, **do not fake the metrics**. Instead, upload the included `test_resume.docx` or a high-quality resume containing a few weak phrasing samples. This will naturally trigger the classifier, ATS matcher, competency tags, and active bullet rewrites.

Save screenshots with these exact filenames in your repository's `/docs/screenshots/` folder.

| Filename | UI Screen / State | What to Display | Real Data Elements to Highlight |
| :--- | :--- | :--- | :--- |
| `01-upload-view.png` | Idle Dropzone | Dropzone container in empty/active state showing the glow and glassmorphic panels. | The drop area showing: *"Drag & Drop your Resume (PDF or DOCX format · up to 5 MB)"*. |
| `02-analyzing-state.png` | Loading Ring | The loading ring spinning while analysis progresses. | The loading step labels: *"Extracting text…"*, *"Predicting role…"*, etc. |
| `03-overview-dashboard.png` | Results Header | Best suitable role, confidence badge, and the ATS rating progress gauge. | The predicted role (e.g. *Python Developer*), model classification confidence, and ATS match score. |
| `04-resume-dna.png` | DNA Profile | Full 5-dimension metrics list with smooth colored status bars. | Technical, Leadership, Impact, Communication, and Problem Solving percentages. |
| `05-skills-matrix.png` | Captured Competencies | Side-by-side grids showing matched (green) vs. missing (red) skills. | The list of matching industry keywords alongside gaps flagged for optimization. |
| `06-directives-polish.png` | Suggestions & Bullets | Algorithmic improvement suggestions list alongside the enhanced work experience bullet points. | Heuristic suggestions and side-by-side passive-to-active rewritten experiences (e.g. *made* → *Engineered*). |
| `07-architecture-flow.png` | Architecture Diagram | A diagram detailing the flow of data across the pipeline. | Render the mermaid diagram from the README as a PNG: *React Upload UI → Flask `/api/analyze` → PDF/DOCX Parser → Preprocessing → TF-IDF Classifier → ATS Matcher → Skill Extractor → Suggestions & Enhanced Bullets → JSON Response to Dashboard*. |

---

## 2. Walkthrough Flow

Your portfolio presentation should walk recruiters through the following sequence:

```
[ Landing Page ]
       ↓
[ Upload File (PDF/DOCX) ]
       ↓
[ Loader Animation (Extracting, Predicting, Matching) ]
       ↓
[ Overview Dashboard (Role & ATS Rating) ]
       ↓
[ Skill Matrix (Competencies vs. Gaps) ]
       ↓
[ Resume DNA Metrics (Genetic Profile) ]
       ↓
[ AI Directives & Polished Action Bullets ]
       ↓
[ System Architecture Flow ]
```

---

## 3. Demo Video Storyboard (Under 90 Seconds)

### Preparation
*   **Resolution**: 1080p (16:9 ratio).
*   **Theme**: Dark mode active.
*   **Sample File**: Prep a sample `.docx` or `.pdf` resume containing typical passive phrases (e.g. *"helped build API"*, *"did database queries"*, *"managed team"*).

### Script & Actions Storyboard

| Time | On-Screen Action | Narration Script |
| :--- | :--- | :--- |
| **0:00 - 0:15** | Open the application page. Drag a sample resume and drop it onto the glow panel. Click *"Enhance with AI"* button. | *"Hi! This is the Nexus AI Resume Builder, an intelligent analyzer built to optimize resumes for modern ATS systems. I'll drop my draft resume, which contains some weak action descriptions, and start the analyzer."* |
| **0:15 - 0:30** | The loading state spinner appears. Point out the steps as they animate (*Extracting text*, *Predicting role*). | *"Behind the scenes, our Flask backend is parsing the document, running clean preprocessing filters, and classifying the profile against 17 industry disciplines."* |
| **0:30 - 0:45** | The success view slides up. Hover over the *"Best Suitable Role"* and *"ATS Match Rating"* cards. | *"And we're done! The machine learning model identifies me as a Python Developer, giving a baseline ATS score of 78% based on similarity vectors."* |
| **0:45 - 1:00** | Scroll to the **Resume DNA Profile** and the **Captured/Missing Skills** grids. | *"We get a detailed DNA metric mapping my technical, leadership, and impact signals, alongside clear badge grids showing which keywords I captured and exactly which critical tags—like Redis or Celery—are missing."* |
| **1:00 - 1:20** | Scroll to the **Enhanced Bullets** card. Highlight the active verb modifications (*made* → *Engineered*). | *"Finally, our heuristic engine reviews my experience bullets, instantly upgrading passive phrasing like 'made' or 'worked on' into high-impact action verbs like 'Engineered' or 'Spearheaded' to grab recruiter attention."* |
| **1:20 - 1:30** | Scroll back up to the dashboard overview and conclude. | *"Nexus AI makes it easy to debug your resume and optimize it for your target role. Check out the setup guide in the README to run it locally. Thanks for watching!"* |

---

## 4. Final Demo Recording Checklist
*   [ ] **Clean State**: Ensure the browser window is zoomed appropriately (100% or 110%) and developer console logs are hidden.
*   [ ] **Server Active**: Flask server is running locally on port 5000.
*   [ ] **Realistic File**: Ready test file is located on the Desktop for easy drag-and-drop.
*   [ ] **Smooth Transitions**: Verify the `.dna-bar-fill` progress animations and hover translations render smoothly.
*   [ ] **Timing Guard**: Time your narration to keep the entire walk under 90 seconds.

---

## 5. Completed 15-Minute UI Polish

The following CSS classes have been successfully integrated:
1.  **Breathing Loading Glow**: Added `pulse-glow` to the `.loading-ring` container.
2.  **DNA Bar Easing**: Progress bars use the transition:
    ```css
    .dna-bar-fill {
      transition: width 1.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    ```
3.  **Card Lift Interactions**: Hover lifts added using standard classes:
    ```css
    .glass-panel {
      transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    .glass-panel:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }
    ```
