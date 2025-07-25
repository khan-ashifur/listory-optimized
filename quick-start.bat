@echo off
echo ================================
echo    LISTORY AI - QUICK START
echo ================================
echo.

echo [1/4] Setting up Python virtual environment...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment. Make sure Python is installed.
        echo Download Python from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo [2/4] Installing Python dependencies...
call venv\Scripts\activate
pip install -q -r ../requirements-basic.txt

echo [3/4] Setting up database...
if not exist ".env" (
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit backend\.env file and add your OpenAI API key
    echo Get your key from: https://platform.openai.com/api-keys
    echo.
)

python manage.py migrate

echo [4/4] Starting Django server...
echo.
echo ================================
echo   SERVER STARTING SUCCESSFULLY
echo ================================
echo Backend API: http://localhost:8000/api/
echo Frontend:   http://localhost:3000
echo.
echo Now open another terminal and run: npm start (in frontend directory)
echo.

python manage.py runserver 0.0.0.0:8000