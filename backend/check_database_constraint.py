import os
import sys
import django
import sqlite3

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

print("CHECKING DATABASE SCHEMA FOR MARKETPLACE CONSTRAINT")
print("=" * 55)

# Connect directly to SQLite database
db_path = os.path.join(backend_path, 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get the actual table schema
cursor.execute("PRAGMA table_info(core_product);")
columns = cursor.fetchall()

print("CORE_PRODUCT TABLE COLUMNS:")
print("-" * 30)
for col in columns:
    print(f"  {col[1]} ({col[2]}) - {col[5] if col[5] else 'No constraint'}")

# Get constraints specifically
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='core_product';")
create_sql = cursor.fetchone()[0]

print("\nCREATE TABLE SQL:")
print("-" * 20)
print(create_sql)

# Check if 'etsy' is in the constraint
if 'etsy' in create_sql:
    print("\n✅ ETSY FOUND in database constraint!")
else:
    print("\n❌ ETSY NOT FOUND in database constraint!")
    print("   This explains why the API rejects 'etsy'")

conn.close()

print("\n" + "=" * 55)
print("DATABASE CHECK COMPLETE")