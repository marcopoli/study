@echo off
echo Starting Univox - Intelligent Study Assistant...
echo.

cd system

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in system\venv.
    echo Please run setup_env.bat first in the system folder.
    pause
    exit /b
)

echo Activating virtual environment...
call venv\Scripts\activate.ps1

echo Launching Streamlit frontend...
streamlit run streamlit_frontend.py

pause
