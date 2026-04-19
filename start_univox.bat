@echo off
echo Avvio di Univox - Intelligent Study Assistant...
echo.

cd system

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo [ERRORE] Ambiente virtuale non trovato in system\venv.
    echo Per favore, esegui prima setup_env.bat nella cartella system.
    pause
    exit /b
)

echo Attivazione ambiente virtuale...
call venv\Scripts\activate.ps1

echo Avvio del frontend Streamlit...
streamlit run streamlit_frontend.py

pause
