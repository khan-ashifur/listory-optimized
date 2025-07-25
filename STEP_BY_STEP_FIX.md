# 🔧 STEP-BY-STEP FIX FOR YOUR ERROR

## Current Issue:
- You're in the `backend` directory
- The batch files are in the root directory
- Django/Celery dependencies aren't installed

## 🚀 SOLUTION (Copy and paste these commands):

### Step 1: Navigate to the correct directory
```bash
cd ..
```
(This takes you back to the main listory-ai folder)

### Step 2: Check what's in the directory
```bash
dir
```
You should see files like `start-basic.bat`, `quick-start.bat`, etc.

### Step 3: Run the basic setup
```bash
start-basic.bat
```

## 🛠️ ALTERNATIVE: Manual Setup (if batch files don't work)

### Option A: Quick Manual Install
```bash
# From the main listory-ai directory
cd backend
pip install Django==5.1.3 djangorestframework==3.15.2 django-cors-headers==4.6.0 python-decouple==3.8 openai==1.57.0 requests==2.32.3 Pillow==11.0.0
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

### Option B: Use Virtual Environment (Recommended)
```bash
# From the main listory-ai directory
cd backend
python -m venv venv
venv\Scripts\activate
pip install Django==5.1.3 djangorestframework==3.15.2 django-cors-headers==4.6.0 python-decouple==3.8 openai==1.57.0 requests==2.32.3 Pillow==11.0.0
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

## 📝 What Each Command Does:

1. **`cd ..`** - Goes back to main directory
2. **`python -m venv venv`** - Creates virtual environment
3. **`venv\Scripts\activate`** - Activates virtual environment
4. **`pip install ...`** - Installs only essential packages (no Celery)
5. **`copy .env.example .env`** - Creates environment file
6. **`python manage.py migrate`** - Sets up database
7. **`python manage.py runserver`** - Starts the server

## ✅ Expected Result:
```
System check identified no issues (0 silenced).
Django version 5.1.3
Starting development server at http://127.0.0.1:8000/
```

## 🚨 If You Still Get Errors:

### Error: "Python is not recognized"
- Install Python from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH"

### Error: "django module not found"
- Make sure you activated the virtual environment: `venv\Scripts\activate`
- You should see `(venv)` at the start of your command prompt

### Error: Still getting Celery errors
- Delete the `__pycache__` folders: `rmdir /s backend\listory\__pycache__`
- Try again

## 🎯 Quick Test:
Once the server starts, visit: http://localhost:8000/api/
You should see a browsable API interface.

## 📞 Need Help?
If you're still having issues, tell me:
1. What directory you're currently in (`pwd` or `cd`)
2. What you see when you run `dir` or `ls`
3. The exact error message you get