# Listory AI - Setup Guide

## Quick Start (Windows)

### 1. Start the Backend Server
Double-click `start-backend.bat` or run in terminal:
```bash
./start-backend.bat
```

### 2. Start the Frontend
Double-click `start-frontend.bat` or run in terminal:
```bash
./start-frontend.bat
```

### 3. Start Celery Worker (for image generation)
Double-click `start-celery.bat` or run in terminal:
```bash
./start-celery.bat
```

## Manual Setup

### Backend Setup
1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate virtual environment:
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```

4. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

5. Copy environment file:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Mac/Linux
   ```

6. Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-openai-api-key
   ```

7. Run migrations:
   ```bash
   python manage.py migrate
   ```

8. Start Django server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start React development server:
   ```bash
   npm start
   ```

### Celery Setup (for image generation)
1. Install Redis (required for Celery):
   - Windows: Download from https://redis.io/download
   - Mac: `brew install redis`
   - Ubuntu: `sudo apt-get install redis-server`

2. Start Redis server:
   ```bash
   redis-server
   ```

3. Start Celery worker:
   ```bash
   cd backend
   celery -A listory worker -l info
   ```

## URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/

## Features
- ✅ AI-powered listing generation for multiple platforms
- ✅ Product image upload for accurate AI image generation
- ✅ Background image generation with 5 types:
  - Hero shot
  - Infographic
  - Lifestyle
  - Testimonial
  - What's in the box
- ✅ Real-time image generation status
- ✅ Platform-specific optimization (Amazon, Walmart, Etsy, TikTok, Shopify)

## Troubleshooting

### Connection Refused Error
If you see `ERR_CONNECTION_REFUSED`, make sure:
1. Django backend is running on port 8000
2. No other application is using port 8000
3. Check the console for any error messages

### Image Generation Not Working
1. Ensure Redis is running
2. Ensure Celery worker is started
3. Check your OpenAI API key is valid
4. Check OpenAI account has credits

### API Key Issues
1. Get your API key from: https://platform.openai.com/api-keys
2. Make sure the key starts with `sk-`
3. Ensure your OpenAI account has sufficient credits