# 🚨 TROUBLESHOOTING GUIDE

## ERROR: `ERR_CONNECTION_REFUSED` or `Network Error`

This means the backend server is not running. Follow these steps:

### 🔧 **Quick Fix (Recommended)**

1. **Check Requirements First:**
   ```bash
   # Double-click this file to check if Python and Node.js are installed
   check-requirements.bat
   ```

2. **Start Backend Server:**
   ```bash
   # Double-click this file - it will set up everything automatically
   quick-start.bat
   ```

3. **Start Frontend (in another terminal):**
   ```bash
   # Double-click this file
   start-frontend-only.bat
   ```

### 🔍 **Manual Debugging**

#### Step 1: Check if Python is installed
```bash
python --version
```
If this fails, install Python from: https://www.python.org/downloads/
**Important:** Check "Add Python to PATH" during installation

#### Step 2: Check if Node.js is installed
```bash
node --version
npm --version
```
If this fails, install Node.js from: https://nodejs.org/

#### Step 3: Start Backend Manually
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install Django djangorestframework django-cors-headers python-decouple openai
python manage.py migrate
python manage.py runserver
```

#### Step 4: Start Frontend Manually
```bash
cd frontend
npm install
npm start
```

### 🚀 **Expected Results**

When working correctly, you should see:

**Backend (Terminal 1):**
```
System check identified no issues (0 silenced).
Django version 5.1.3
Starting development server at http://127.0.0.1:8000/
```

**Frontend (Terminal 2):**
```
Local:            http://localhost:3000
On Your Network:  http://192.168.x.x:3000
```

### 🔗 **URL Check**

- Frontend: http://localhost:3000 ✅ Should show Listory AI landing page
- Backend API: http://localhost:8000/api/ ✅ Should show API endpoints
- Backend Admin: http://localhost:8000/admin/ ✅ Should show Django admin

### ⚠️ **Common Issues**

#### Issue: "Python is not recognized"
**Solution:** Install Python and make sure "Add to PATH" is checked

#### Issue: "Node is not recognized"  
**Solution:** Install Node.js from nodejs.org

#### Issue: "Permission denied"
**Solution:** Run as Administrator or check antivirus settings

#### Issue: "Port already in use"
**Solution:** Kill existing process:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F

# Or use different port
python manage.py runserver 8001
```

#### Issue: "Module not found"
**Solution:** Activate virtual environment:
```bash
cd backend
venv\Scripts\activate
pip install -r ../requirements.txt
```

### 🆘 **Still Not Working?**

1. **Use Mock Server (Temporary):**
   ```bash
   cd backend
   python simple_server.py
   ```

2. **Check Firewall/Antivirus:**
   - Allow Python and Node.js through firewall
   - Temporarily disable antivirus

3. **Try Different Ports:**
   ```bash
   # Backend on different port
   python manage.py runserver 8001
   
   # Update frontend API URL in src/services/api.js
   const API_BASE_URL = 'http://localhost:8001/api';
   ```

4. **Clean Installation:**
   ```bash
   # Delete and recreate
   rmdir /s backend\venv
   rmdir /s frontend\node_modules
   # Then run quick-start.bat again
   ```

### 📞 **Need Help?**

If you're still having issues:
1. Run `check-requirements.bat` and share the output
2. Share any error messages you see
3. Confirm your operating system version

The app should work on Windows 10/11 with Python 3.8+ and Node.js 16+.