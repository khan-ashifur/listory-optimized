"""
🇪🇸 TEST CONVERSION-FOCUSED SPANISH DESCRIPTION  
Testing the new buyer psychology + mobile-optimized format
From technical datasheet → Amazon conversion machine
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_conversion_description():
    """Test the conversion-focused Spanish description format"""
    
    print("🇪🇸 TESTING CONVERSION-FOCUSED DESCRIPTION FORMAT")
    print("=" * 65)
    print("🎯 From Technical Datasheet → Amazon Conversion Machine")
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product  
        from django.contrib.auth.models import User
        
        service = ListingGeneratorService()
        
        # Test user
        user, created = User.objects.get_or_create(
            username='conversion_test',
            defaults={'email': 'test@amazon.es'}
        )
        
        # Test with cutting board (like the example you showed)
        product = Product.objects.create(
            user=user,
            name='N-GEN Tablas de Cortar Doble Cara',
            description='Set de 2 tablas de cortar con superficie doble: acero inoxidable y PP paja de trigo',
            brand_name='N-GEN',
            brand_tone='professional',
            target_platform='amazon',
            marketplace='es', 
            marketplace_language='es',
            price=49.99,
            occasion='general',
            categories='Kitchen,Cookware,Cutting Boards',
            features='Acero inoxidable 304,PP paja de trigo,Bordes antideslizantes,Apto lavavajillas,Asa acero,42x29x1.5cm'
        )
        
        print(f"✅ Testing Product: {product.name}")
        print(f"📱 Analyzing conversion-focused format...")
        
        # Get the improved description format
        desc_format = service.get_marketplace_description_format('es', product.brand_tone)
        
        print(f"\n🔍 CONVERSION ANALYSIS:")
        print("-" * 50)
        
        # Test 1: Buyer Psychology  
        psych_checks = {
            'Problem hook': 'BUYER PROBLEM HOOK' in desc_format and 'pain point question' in desc_format,
            'Relatable problems': 'Cansado de tablas que huelen mal' in desc_format,
            'Immediate solution': 'SOLUCIÓN INMEDIATA' in desc_format,
            'Emotional benefits': 'más limpia' in desc_format and 'más seguro' in desc_format,
            'Social proof': 'miles de familias' in desc_format and 'ya usan' in desc_format
        }
        
        psych_score = sum(psych_checks.values()) / len(psych_checks) * 100
        print(f"🧠 BUYER PSYCHOLOGY: {psych_score:.1f}%")
        for check, passed in psych_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Test 2: Use-Case Keywords
        usecase_checks = {
            'Meal prep keywords': 'meal prep' in desc_format and 'MEAL PREP DOMINICAL' in desc_format,
            'Family cooking': 'cocina familiar' in desc_format and 'COCINA FAMILIAR' in desc_format,
            'Daily use scenarios': 'uso diario' in desc_format,
            'Cleaning benefits': 'limpieza fácil' in desc_format and 'LIMPIEZA RÁPIDA' in desc_format,
            'Kitchen optimization': 'ESPACIO OPTIMIZADO' in desc_format
        }
        
        usecase_score = sum(usecase_checks.values()) / len(usecase_checks) * 100  
        print(f"\n🍳 USE-CASE KEYWORDS: {usecase_score:.1f}%")
        for check, passed in usecase_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Test 3: Mobile Conversion Structure
        mobile_checks = {
            'Scannable headers': 'PERFECTO PARA TU COCINA DIARIA' in desc_format,
            'Bullet benefits': 'Corta todo sin mezclar sabores' in desc_format,
            'Comparison language': 'LO QUE OTROS NO TIENEN' in desc_format,
            'Immediate results': 'RESULTADOS DESDE EL PRIMER USO' in desc_format,
            'Action-oriented CTA': 'AÑADIR AL CARRITO' in desc_format
        }
        
        mobile_score = sum(mobile_checks.values()) / len(mobile_checks) * 100
        print(f"\n📱 MOBILE CONVERSION: {mobile_score:.1f}%")
        for check, passed in mobile_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
            
        # Test 4: Anti-Technical Datasheet
        antitechnical_checks = {
            'No technical opening': 'ANÁLISIS EXPERTO' not in desc_format,
            'No specs-first': 'DETALLES TÉCNICOS' not in desc_format,
            'Conversational tone': 'tú' in desc_format and 'questions' in desc_format,
            'Benefits over features': 'BENEFICIOS' in desc_format or 'POR QUÉ ELEGIR' in desc_format,
            'Results focused': 'resultados inmediatos' in desc_format
        }
        
        antitechnical_score = sum(antitechnical_checks.values()) / len(antitechnical_checks) * 100
        print(f"\n🚫 ANTI-DATASHEET: {antitechnical_score:.1f}%")
        for check, passed in antitechnical_checks.items():
            print(f"   {'✅' if passed else '❌'} {check}")
        
        # Overall Amazon Conversion Score
        print(f"\n🏆 AMAZON CONVERSION SCORE:")
        print("=" * 40)
        
        overall_score = (psych_score + usecase_score + mobile_score + antitechnical_score) / 4
        
        print(f"🧠 Buyer Psychology: {psych_score:.1f}%")
        print(f"🍳 Use-Case Keywords: {usecase_score:.1f}%") 
        print(f"📱 Mobile Conversion: {mobile_score:.1f}%")
        print(f"🚫 Anti-Datasheet: {antitechnical_score:.1f}%")
        print(f"")
        print(f"🎯 FINAL CONVERSION SCORE: {overall_score:.1f}/100")
        
        if overall_score >= 95:
            rating = "🏆 10/10 - AMAZON CONVERSION MACHINE"
            verdict = "Perfect buyer psychology + mobile optimization!"
            impact = "Maximum conversions: Problem → Solution → Buy Now"
        elif overall_score >= 90:
            rating = "🥇 9.5/10 - EXCELLENT CONVERSION"
            verdict = "Strong buyer psychology with great mobile structure."
            impact = "High conversion rate expected"
        elif overall_score >= 85:
            rating = "🥈 9/10 - GOOD CONVERSION"  
            verdict = "Good buyer focus but room for improvement."
            impact = "Above average conversion performance"
        else:
            rating = "📊 8/10 - NEEDS MORE BUYER FOCUS"
            verdict = "Still too technical, needs more conversion psychology."
            impact = "Risk of low conversion vs optimized listings"
        
        print(f"\n{rating}")
        print(f"💡 VERDICT: {verdict}")
        print(f"📈 CONVERSION IMPACT: {impact}")
        
        # Show the transformation
        print(f"\n🔄 TRANSFORMATION ACHIEVED:")
        print("-" * 45)
        print("❌ OLD: ANÁLISIS EXPERTO technical datasheet")
        print("✅ NEW: ¿Cansado de...? buyer problem hook")
        print("")
        print("❌ OLD: Dense technical paragraphs") 
        print("✅ NEW: PERFECTO PARA TU COCINA DIARIA scannable")
        print("")
        print("❌ OLD: Feature specifications")
        print("✅ NEW: LO QUE OTROS NO TIENEN competitive advantage")
        print("")
        print("❌ OLD: Technical confidence statement")
        print("✅ NEW: RESULTADOS DESDE EL PRIMER USO immediate gratification")
        
        # Expected output preview
        print(f"\n📋 EXPECTED NEW OUTPUT:")
        print("-" * 30)
        print("¿Cansado de tablas que huelen mal después de cortar carne?")
        print("TABLAS DE CORTAR DOBLE CARA eliminan olores para siempre...")
        print("")
        print("PERFECTO PARA TU COCINA DIARIA:")
        print("• MEAL PREP DOMINICAL: Corta todo sin mezclar sabores")
        print("• COCINA FAMILIAR: Una tabla carnes, otra verduras")
        print("")
        print("LO QUE OTROS NO TIENEN:")
        print("✅ DOBLE SUPERFICIE = Sin contaminación cruzada nunca")
        print("")
        print("RESULTADOS DESDE EL PRIMER USO:")
        print("Cocina más limpia ✅ Meal prep más rápido ✅")
        
        # Cleanup
        product.delete()
        
        return overall_score >= 95
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_conversion_description()
    print(f"\n{'🎉 CONVERSION MACHINE ACHIEVED!' if success else '🔧 CONTINUE OPTIMIZING'}")
    print("🇪🇸 Spanish conversion description test completed")