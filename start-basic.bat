@echo off
echo ================================
echo    LISTORY AI - BASIC START
echo    (Without Celery - Images will generate synchronously)
echo ================================
echo.

echo [1/3] Setting up Python environment...
cd backend
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Make sure Python is installed: https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

echo [2/3] Installing core dependencies...
call venv\Scripts\activate
pip install -q Django==5.1.3 djangorestframework==3.15.2 django-cors-headers==4.6.0 python-decouple==3.8 openai==1.57.0 requests==2.32.3 Pillow==11.0.0

echo [3/3] Setting up database and starting server...
if not exist ".env" (
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit backend\.env and add your OpenAI API key
    echo Get your key from: https://platform.openai.com/api-keys
    echo.
)

python manage.py migrate

echo.
echo ================================
echo   SERVER STARTING
echo ================================
echo Backend API: http://localhost:8000/api/
echo.
echo NOTE: Images will generate synchronously (may take longer)
echo For faster async image generation, install Redis and Celery
echo.

python manage.py runserver 0.0.0.0:8000