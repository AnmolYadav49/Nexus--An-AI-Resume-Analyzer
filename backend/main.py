from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile, File, HTTPException
import parser
import ai_service

app = FastAPI(title="AI Resume Builder API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Resume Builder Backend is running!"}

@app.get("/test-ai")
def test_ai():
    """
    Tests the connection to the local Ollama instance.
    Make sure Ollama is running on your machine and you have Llama 3.1 installed.
    """
    result = ai_service.test_connection()
    return {"local_ai_status": result}

@app.post("/api/upload")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        contents = await file.read()
        extracted_text = parser.extract_text_from_pdf(contents)
        
        improved_resume = ai_service.enhance_resume(extracted_text)
        
        return {
            "original_text": extracted_text,
            "improved_resume": improved_resume
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
