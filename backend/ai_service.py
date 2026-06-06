import ollama

def test_connection(model_name="llama3.1"):
    try:
        response = ollama.chat(model=model_name, messages=[
            {
                'role': 'user',
                'content': 'Hello! Respond with a simple "Yes, I am running locally!" if you can hear me.'
            }
        ])
        return {
            "success": True,
            "response": response['message']['content'],
            "model": model_name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "troubleshooting": f"Ensure Ollama is running and `{model_name}` is downloaded."
        }

import json

def enhance_resume(resume_text: str, model_name="llama3.1"):
    prompt = f"""
You are an expert resume writer and career coach.
I will give you the raw text of a resume. 
Your task is to organize and rewrite this resume to be highly impactful, quantifying achievements, and organizing it cleanly.
Return the output ONLY as a valid JSON object with the exact following keys:
{{
  "personal_info": {{"name": "", "email": "", "phone": "", "linkedin": ""}},
  "summary": "A powerful professional summary",
  "experience": [
    {{"company": "", "role": "", "duration": "", "achievements": ["impactful bullet 1", "impactful bullet 2"]}}
  ],
  "education": [
    {{"institution": "", "degree": "", "duration": "", "details": ""}}
  ],
  "skills": ["skill 1", "skill 2"]
}}

Raw Resume:
{resume_text}
"""
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        return json.loads(response['message']['content'])
    except Exception as e:
        return {"error": str(e)}
