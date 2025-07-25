@echo off
echo Starting Listory AI Backend Server...
echo.

cd backend

echo Checking if virtual environment exists...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r ../requirements.txt

echo Running migrations...
python manage.py migrate

echo Starting Django development server...
echo Backend will be available at: http://localhost:8000
echo API endpoints at: http://localhost:8000/api/
echo.
python manage.py runserver

pause