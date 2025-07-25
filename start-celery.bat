@echo off
echo Starting Celery Worker for Image Generation...
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting Celery worker...
echo This will handle background image generation tasks
echo.
celery -A listory worker -l info

pause