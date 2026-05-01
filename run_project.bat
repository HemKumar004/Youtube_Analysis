@echo off
echo Starting YouTube AI Automation Platform...

echo Starting backend server...
start cmd /k "cd backend && .\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000"

echo Starting frontend server...
start cmd /k "cd frontend && npm run dev"

echo Both servers are starting in new windows.
echo Frontend will be available at http://localhost:5173/
echo Backend will be available at http://localhost:8000/api
pause
