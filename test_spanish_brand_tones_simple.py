"""
Simple test to verify Spanish brand tones are working correctly
"""

import os
import sys
import django
import random

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_all_spanish_brand_tones():
    """Test all Spanish brand tones systematically"""
    
    print("🇪🇸 TESTING ALL SPANISH BRAND TONES")
    print("=" * 50)
    
    try:
        from apps.listings.brand_tone_optimizer import BrandToneOptimizer
        
        optimizer = BrandToneOptimizer()
        brand_tones = ['professional', 'casual', 'luxury', 'playful', 'minimal', 'bold']
        
        expected_labels = {
            'professional': ['RENDIMIENTO PROFESIONAL:', 'INGENIERÍA EXPERTA:', 'CONFIABILIDAD PROBADA:'],
            'casual': ['SÚPER FÁCIL DE USAR:', 'TE VA A ENCANTAR:', 'SIMPLEMENTE PERFECTO PARA:'],
            'luxury': ['ARTESANÍA PREMIUM:', 'EXPERIENCIA DE LUJO:', 'DISEÑO ELEGANTE:'],
            'playful': ['REALMENTE INCREÍBLE:', 'DISEÑO INTELIGENTE:', 'SORPRENDENTEMENTE BUENO:'],
            'minimal': ['SIMPLEMENTE FUNCIONA:', 'DISEÑO LIMPIO:', 'RENDIMIENTO PURO:'],
            'bold': ['POTENCIA MÁXIMA:', 'LIBERA EL RENDIMIENTO:', 'DOMINA CON:']
        }
        
        results = {}
        
        for brand_tone in brand_tones:
            print(f"\n🎨 Testing {brand_tone.upper()}:")
            
            # Test multiple times to account for randomness
            spanish_found = False
            
            for attempt in range(5):  # Try 5 times to account for random selection
                random.seed(attempt)  # Different seed each time
                enhancement = optimizer.get_brand_tone_enhancement(brand_tone, 'es')
                
                # Check if any expected Spanish labels appear
                expected = expected_labels[brand_tone]
                found_labels = [label for label in expected if label in enhancement]
                
                if found_labels:
                    spanish_found = True
                    print(f"   ✅ Attempt {attempt + 1}: Found Spanish labels: {found_labels}")
                    break
                else:
                    print(f"   ⚠️ Attempt {attempt + 1}: No Spanish labels found")
            
            results[brand_tone] = spanish_found
            
            if not spanish_found:
                print(f"   ❌ {brand_tone.upper()}: Spanish labels not working")
                # Debug: check if Spanish labels exist in config
                config = optimizer.tone_configurations[brand_tone]
                has_spanish = 'bullet_labels_es' in config
                print(f"   🔍 Config has Spanish labels: {has_spanish}")
                if has_spanish:
                    print(f"   📝 Available Spanish labels: {config['bullet_labels_es'][:2]}")
            else:
                print(f"   ✅ {brand_tone.upper()}: Spanish labels working correctly")
        
        # Summary
        print(f"\n📊 SPANISH BRAND TONE TEST RESULTS:")
        print("=" * 50)
        
        working_count = sum(results.values())
        total_count = len(results)
        success_rate = (working_count / total_count) * 100
        
        for tone, working in results.items():
            status = "✅ Working" if working else "❌ Failed"
            print(f"   {tone.capitalize()}: {status}")
        
        print(f"\n🏆 SUCCESS RATE: {working_count}/{total_count} ({success_rate:.1f}%)")
        
        if success_rate >= 100:
            print("🎉 PERFECT! All Spanish brand tones working correctly!")
        elif success_rate >= 80:
            print("🎯 GOOD! Most Spanish brand tones working, minor fixes needed.")
        else:
            print("🔧 NEEDS WORK! Significant issues with Spanish brand tones.")
        
        return success_rate >= 100
        
    except Exception as e:
        print(f"❌ Error testing Spanish brand tones: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_all_spanish_brand_tones()
    print(f"\n{'SUCCESS' if success else 'NEEDS MORE WORK'}: Spanish brand tone testing {'completed perfectly' if success else 'needs refinement'}!")