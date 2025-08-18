import os, sys, django

# Set up Django
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing
listing = GeneratedListing.objects.get(id=976)
print('🇹🇷 TURKEY A+ CONTENT SAMPLE:')
print('=' * 60)
content = listing.amazon_aplus_content
print(content[:2000])
print('...')
print(f'📊 Total: {len(content)} characters')