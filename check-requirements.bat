@echo off
echo ================================
echo   CHECKING SYSTEM REQUIREMENTS
echo ================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please download and install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    goto :node_check
) else (
    echo ✓ Python is installed
)
echo.

:node_check
echo Checking Node.js installation...
node --version
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please download and install Node.js from: https://nodejs.org/
    echo.
) else (
    echo ✓ Node.js is installed
)

echo.
echo Checking npm...
npm --version
if errorlevel 1 (
    echo ERROR: npm is not available
) else (
    echo ✓ npm is available
)

echo.
echo ================================
echo   SYSTEM CHECK COMPLETE
echo ================================
echo.
echo If both Python and Node.js are installed, you can run:
echo 1. quick-start.bat (for backend)
echo 2. start-frontend-only.bat (for frontend)
echo.
pause