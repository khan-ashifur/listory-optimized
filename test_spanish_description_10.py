"""
🇪🇸 TEST SPANISH DESCRIPTION 10/10 OPTIMIZATION
Testing the new mobile-first, SEO-optimized Spanish description format
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_spanish_description_10():
    """Test the new 10/10 Spanish description format"""
    
    print("🇪🇸 TESTING SPANISH DESCRIPTION 10/10 FORMAT")
    print("=" * 60)
    print("🎯 Mobile-first + SEO + Scannable optimization")
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        
        service = ListingGeneratorService()
        
        # Get or create test user
        user, created = User.objects.get_or_create(
            username='spanish_desc_test',
            defaults={'email': 'test@amazon.es'}
        )
        
        # Test with the Sensei earbuds example
        product = Product.objects.create(
            user=user,
            name='Sensei Auriculares Bluetooth Premium',
            description='Auriculares inalámbricos profesionales con cancelación de ruido activa',
            brand_name='Sensei',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='es',
            marketplace_language='es',
            price=89.99,
            occasion='general',
            categories='Electronics,Audio,Headphones',
            features='Cancelación ruido ANC -35dB,Batería 30 horas,Bluetooth 5.3 alcance 15m,Carga rápida USB-C 2h,IPX5 resistente sudor'
        )
        
        print(f"✅ Product: {product.name}")
        print(f"📱 Testing new Spanish description format...")
        
        # Get the new description format
        desc_format = service.get_marketplace_description_format('es', product.brand_tone)
        
        print(f"\n🔍 ANALYZING DESCRIPTION FORMAT:")
        print("-" * 50)
        
        # Test 1: Mobile Optimization
        mobile_checks = {
            'Paragraph headers': any(header in desc_format for header in ['PÁRRAFO 1', 'PÁRRAFO 2', 'PÁRRAFO 3', 'PÁRRAFO 4']),
            'CAPS headers': 'CAPS HEADER' in desc_format,
            'Mobile scanning': 'MOBILE SCANNING' in desc_format,
            'Bullet points': '•' in desc_format and '✅' in desc_format and '➤' in desc_format,
            'Paragraph spacing': '\\n\\n' in desc_format
        }
        
        mobile_score = sum(mobile_checks.values()) / len(mobile_checks) * 100
        print(f"📱 MOBILE OPTIMIZATION: {mobile_score:.1f}%")
        for check, passed in mobile_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Test 2: SEO Optimization
        seo_checks = {
            'Keyword density': 'KEYWORD DENSITY' in desc_format and 'appears 3-4 times' in desc_format,
            'Keyword reinforcement': 'REPEAT 2-3 MAIN KEYWORDS' in desc_format,
            'Category keywords': 'category keywords' in desc_format,
            'SEO rules section': 'CRITICAL SEO' in desc_format,
            'Spanish buying signals': 'envío España' in desc_format and 'garantía' in desc_format,
            'Numbers emphasis': 'specific numbers' in desc_format
        }
        
        seo_score = sum(seo_checks.values()) / len(seo_checks) * 100
        print(f"\n🎯 SEO OPTIMIZATION: {seo_score:.1f}%")
        for check, passed in seo_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Test 3: Scannability
        scan_checks = {
            'Clear structure': 'MANDATORY STRUCTURE' in desc_format,
            'Character limits': '250 chars' in desc_format and '400 chars' in desc_format,
            'Scannable headers': 'HOOK + KEYWORDS' in desc_format and 'SPECS SCANEABLES' in desc_format,
            'Visual hierarchy': '🎯' in desc_format and '🔥' in desc_format and '⭐' in desc_format and '🛒' in desc_format,
            'Action words': 'AÑADIR AL CARRITO' in desc_format and 'DISPONIBLE' in desc_format
        }
        
        scan_score = sum(scan_checks.values()) / len(scan_checks) * 100
        print(f"\n👁️ SCANNABILITY: {scan_score:.1f}%")
        for check, passed in scan_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Test 4: Amazon Algorithm Optimization
        amazon_checks = {
            'Algorithm-friendly': 'Amazon algorithm-friendly' in desc_format,
            'Conversion optimization': 'conversion-optimized' in desc_format,
            'Spain-specific trust': 'certificado CE' in desc_format and 'garantía europea' in desc_format,
            'Local shipping': 'envío España' in desc_format,
            'Urgency signals': 'LIMITADA' in desc_format and 'hoy' in desc_format,
            'No fluff rule': 'NO FLUFF' in desc_format and 'Every word serves SEO' in desc_format
        }
        
        amazon_score = sum(amazon_checks.values()) / len(amazon_checks) * 100
        print(f"\n🏪 AMAZON ALGORITHM: {amazon_score:.1f}%")
        for check, passed in amazon_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Overall 10/10 Assessment
        print(f"\n🏆 OVERALL 10/10 ASSESSMENT:")
        print("=" * 40)
        
        overall_score = (mobile_score + seo_score + scan_score + amazon_score) / 4
        
        print(f"📱 Mobile Optimization: {mobile_score:.1f}%")
        print(f"🎯 SEO Optimization: {seo_score:.1f}%") 
        print(f"👁️ Scannability: {scan_score:.1f}%")
        print(f"🏪 Amazon Algorithm: {amazon_score:.1f}%")
        print(f"")
        print(f"🎯 FINAL DESCRIPTION QUALITY: {overall_score:.1f}/100")
        
        if overall_score >= 95:
            rating = "🏆 10/10 - PERFECT DESCRIPTION FORMAT"
            verdict = "Amazon mobile + SEO + conversion optimized to perfection!"
            impact = "Expected: Maximum mobile readability + algorithm ranking + conversions"
        elif overall_score >= 90:
            rating = "🥇 9.5/10 - NEAR PERFECT"
            verdict = "Excellent optimization with minor room for improvement."
            impact = "Expected: High mobile engagement + strong SEO performance"
        elif overall_score >= 85:
            rating = "🥈 9/10 - VERY GOOD"
            verdict = "Strong optimization but missing some key elements."
            impact = "Expected: Good mobile experience + decent SEO"
        else:
            rating = "🥉 8.5/10 - NEEDS MORE WORK"
            verdict = "Foundation is good but needs more optimization."
            impact = "Expected: Basic mobile readability"
        
        print(f"\n{rating}")
        print(f"💡 VERDICT: {verdict}")
        print(f"📈 IMPACT: {impact}")
        
        # Key improvements made
        print(f"\n✅ KEY IMPROVEMENTS vs OLD FORMAT:")
        print("-" * 45)
        print("✓ MOBILE-FIRST: Clear scannable structure with CAPS headers")
        print("✓ SEO-OPTIMIZED: Keyword density + reinforcement rules") 
        print("✓ AMAZON ALGORITHM: Spain-specific trust signals + urgency")
        print("✓ NO FLUFF: Every word serves SEO or conversion purpose")
        print("✓ VISUAL HIERARCHY: Emojis + bullets + spacing for mobile")
        print("✓ ACTION-ORIENTED: Clear CTA + urgency + value propositions")
        
        # Expected output example
        print(f"\n📋 EXPECTED OUTPUT EXAMPLE:")
        print("-" * 30)
        print("AURICULARES BLUETOOTH INALÁMBRICOS con CANCELACIÓN RUIDO ANC profesional...")
        print("")
        print("ESPECIFICACIONES PREMIUM:")
        print("• BATERÍA: 30h reproducción + 2h carga USB-C")
        print("• AUDIO: Cancelación ruido ANC -35dB certificada")
        print("")
        print("GARANTÍA ESPAÑA + CALIDAD EUROPEA:")
        print("✅ ENVÍO DESDE ESPAÑA 24-48h")
        print("✅ CERTIFICADO CE/FCC seguridad europea")
        print("")
        print("OFERTA LIMITADA AMAZON: Precio especial hoy...")
        
        # Cleanup
        product.delete()
        
        return overall_score >= 95
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_spanish_description_10()
    print(f"\n{'🎉 10/10 DESCRIPTION FORMAT ACHIEVED!' if success else '🔧 CONTINUE REFINING'}")
    print("🇪🇸 Spanish description optimization completed")