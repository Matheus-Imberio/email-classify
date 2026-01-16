@echo off
echo ========================================
echo   Email Intelligence Classifier
echo ========================================
echo.
echo Iniciando servicos...
echo.

start "Backend" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

start "Frontend" cmd /k "python -m streamlit run app/frontend.py --server.port 8501"

echo.
echo Servicos iniciados!
echo.
echo Backend API:  http://localhost:8000
echo Frontend:     http://localhost:8501
echo API Docs:     http://localhost:8000/docs
echo.
pause

