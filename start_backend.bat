@echo off
echo Starting Django Backend Server...
cd backend
call venv\Scripts\activate
echo.
echo Server starting on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
pause