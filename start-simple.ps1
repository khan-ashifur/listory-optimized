# Simple PowerShell script to start Listory AI
Write-Host "==================================" -ForegroundColor Green
Write-Host "    LISTORY AI - SIMPLE START" -ForegroundColor Green  
Write-Host "==================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (!(Test-Path "backend\manage.py")) {
    Write-Host "ERROR: Please run this from the main listory-ai directory" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host "Expected files: backend\manage.py, frontend\package.json" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/4] Setting up Python environment..." -ForegroundColor Cyan
Set-Location backend

if (!(Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Write-Host "Make sure Python is installed: https://www.python.org/downloads/" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

Write-Host "[3/4] Installing dependencies..." -ForegroundColor Cyan
pip install -q Django==5.1.3 djangorestframework==3.15.2 django-cors-headers==4.6.0 python-decouple==3.8 openai==1.57.0 requests==2.32.3 Pillow==11.0.0

Write-Host "[4/4] Setting up database..." -ForegroundColor Cyan
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "IMPORTANT: Edit backend\.env and add your OpenAI API key" -ForegroundColor Yellow
    Write-Host "Get your key from: https://platform.openai.com/api-keys" -ForegroundColor Yellow
    Write-Host ""
}

python manage.py migrate

Write-Host ""
Write-Host "==================================" -ForegroundColor Green
Write-Host "   SERVER STARTING SUCCESSFULLY" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000/api/" -ForegroundColor Cyan
Write-Host "Now open another terminal and run frontend:" -ForegroundColor Yellow
Write-Host "cd frontend && npm install && npm start" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 0.0.0.0:8000