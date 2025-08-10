import json
import requests

data = {
    'name': 'Test Wireless Headphones',
    'description': 'High-quality wireless headphones',
    'brand_name': 'TechBrand',
    'asin': '',
    'marketplace': 'us',
    'price': '79.99',
    'categories': 'Electronics',
    'features': 'Noise cancellation',
    'brand_tone': 'professional',
    'target_platform': 'amazon',
    'product_urls': ['https://example.com/product'],
    'competitor_urls': [],
    'competitor_asins': [],
    'target_keywords': '',
    'occasion': ''
}

print('Testing API...')
try:
    response = requests.post('http://localhost:8000/api/core/products/', json=data)
    print('Status:', response.status_code)
    if response.status_code \!= 201:
        print('Error:', response.text)
    else:
        print('Success\!')
except Exception as e:
    print('Error:', e)
