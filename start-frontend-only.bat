@echo off
echo ================================
echo    STARTING REACT FRONTEND
echo ================================
echo.

cd frontend

echo Installing Node.js dependencies...
npm install

echo.
echo ================================
echo   FRONTEND STARTING
echo ================================
echo Frontend URL: http://localhost:3000
echo Make sure backend is running on: http://localhost:8000
echo.

npm start