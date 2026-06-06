Write-Host "Starting AI Resume Builder Servers..." -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "-NoExit -Command `"cd 'C:\Users\Anmol Yadav\Desktop\ai-resume-builder\backend'; .\venv\Scripts\Activate.ps1; uvicorn main:app --reload`""

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit -Command `"cd 'C:\Users\Anmol Yadav\Desktop\ai-resume-builder\frontend'; npm run dev`""

Write-Host "Servers should be spinning up in new terminal windows." -ForegroundColor Green
Write-Host "Make sure Ollama is running in the background as well!" -ForegroundColor Yellow
