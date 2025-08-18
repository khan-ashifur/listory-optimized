"""
Quick fix for the 500 error by replacing the problematic services.py temporarily
"""
import os
import shutil

def fix_server():
    # Backup current services.py
    services_path = "backend/apps/listings/services.py"
    backup_path = "backend/apps/listings/services.py.backup"
    
    if os.path.exists(services_path):
        print("Creating backup of services.py...")
        shutil.copy2(services_path, backup_path)
        
        # Read current services.py
        with open(services_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace all print statements to avoid Windows encoding issues
        fixes = [
            ('print(f"AI generation attempt {retry_count + 1}/{max_retries}")', '# print disabled'),
            ('print(f"🚨 OpenAI API error on attempt {retry_count}/{max_retries}")', '# print disabled'),
            ('print(f"[ERROR] OpenAI API error: {e}")', '# print disabled'),
            ('print(', '# print('),  # Comment out all remaining prints
        ]
        
        for old, new in fixes:
            content = content.replace(old, new)
        
        # Write fixed version
        with open(services_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Applied quick fix - all print statements disabled")
        print("✅ Backup saved as services.py.backup")
        return True
    else:
        print("❌ services.py not found")
        return False

if __name__ == "__main__":
    fix_server()