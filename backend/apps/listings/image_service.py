import json
import logging
from django.conf import settings
from .models import ListingImage

try:
    from celery import shared_task
    CELERY_AVAILABLE = True
except ImportError:
    # Celery not installed - define dummy decorator
    def shared_task(func):
        return func
    CELERY_AVAILABLE = False

logger = logging.getLogger(__name__)


class ImageGenerationService:
    def __init__(self):
        try:
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your-openai-api-key-here":
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized for image generation")
            else:
                self.client = None
                logger.warning("OpenAI API key not configured for image generation")
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            self.client = None

    def create_image_prompts(self, listing):
        """Create specific prompts for each image type based on listing data"""
        product = listing.product
        
        # Parse listing data for better prompts
        title = listing.title
        features = listing.bullet_points.split('\n') if listing.bullet_points else []
        
        prompts = {
            'hero': self._create_hero_prompt(product, title, features),
            'infographic': self._create_infographic_prompt(product, features),
            'lifestyle': self._create_lifestyle_prompt(product, title),
            'testimonial': self._create_testimonial_prompt(product),
            'whats_in_box': self._create_whats_in_box_prompt(product)
        }
        
        return prompts

    def _create_hero_prompt(self, product, title, features):
        """Create hero shot prompt"""
        image_reference = ""
        if product.product_image:
            image_reference = f"\nReference the uploaded product image for accurate representation of {product.name}"
        
        return f"""Create a professional hero product photograph of {product.name}.
Style: Clean, modern e-commerce product photography
Background: Pure white or subtle gradient
Lighting: Professional studio lighting with soft shadows
Angle: 3/4 view showing the product's best features
Details: Sharp focus, high-quality rendering showing texture and materials
Brand tone: {product.brand_tone}
Key features to highlight: {', '.join(features[:2]) if features else 'premium quality'}
No text or logos in the image.{image_reference}"""

    def _create_infographic_prompt(self, product, features):
        """Create infographic prompt"""
        return f"""Create a clean, modern infographic for {product.name}.
Style: Minimalist design with icons and visual elements
Layout: Organized grid or flow showing 4-5 key features
Colors: Professional color scheme matching {product.brand_tone} tone
Elements: Use icons, simple illustrations, and visual metaphors
Features to highlight: {', '.join(features[:4]) if features else 'key product benefits'}
Design: Clean typography, plenty of white space, easy to scan
No actual text - use visual representations only."""

    def _create_lifestyle_prompt(self, product, title):
        """Create lifestyle shot prompt"""
        image_reference = ""
        if product.product_image:
            image_reference = f"\nEnsure the product matches the design and features from the uploaded reference image"
        
        return f"""Create a lifestyle photograph showing {product.name} in use.
Setting: Natural, real-world environment where the product would be used
People: Show diverse person(s) happily using or benefiting from the product
Mood: {product.brand_tone}, aspirational, relatable
Lighting: Natural, warm lighting
Composition: Product clearly visible but integrated into the scene
Emotion: Show the positive transformation or benefit
Context: Realistic usage scenario that resonates with target customers.{image_reference}"""

    def _create_testimonial_prompt(self, product):
        """Create testimonial visual prompt"""
        return f"""Create a testimonial-style image for {product.name}.
Style: Split layout or before/after visualization
Elements: Show contrast between problem and solution
Visual metaphor: Represent customer satisfaction and transformation
Mood: Authentic, trustworthy, {product.brand_tone}
Design: Clean, professional layout suggesting social proof
Focus: Visual representation of positive customer experience
No actual text or quotes - use visual storytelling only."""

    def _create_whats_in_box_prompt(self, product):
        """Create what's in the box prompt"""
        image_reference = ""
        if product.product_image:
            image_reference = f"\nEnsure the main product accurately reflects the uploaded reference image"
        
        return f"""Create a flat lay photograph showing {product.name} unboxed.
Style: Organized, aesthetic flat lay photography
Background: Clean, neutral surface (white, wood, or marble)
Layout: Main product centered with accessories/components arranged around it
Items: Show the main product plus any accessories, manual, packaging
Lighting: Soft, even lighting from above, minimal shadows
Composition: Neat, organized, Instagram-worthy arrangement
Details: Each item clearly visible and identifiable.{image_reference}"""

    def generate_image(self, listing_image_id):
        """Generate a single image for a listing"""
        try:
            listing_image = ListingImage.objects.get(id=listing_image_id)
            
            if not self.client:
                listing_image.status = 'failed'
                listing_image.error_message = 'OpenAI API key not configured'
                listing_image.save()
                return
            
            # Update status to generating
            listing_image.status = 'generating'
            listing_image.save()
            
            # Generate image using DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=listing_image.prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            # Save the image URL
            listing_image.image_url = response.data[0].url
            listing_image.status = 'completed'
            listing_image.save()
            
            logger.info(f"Successfully generated {listing_image.image_type} image for listing {listing_image.listing.id}")
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            listing_image.status = 'failed'
            listing_image.error_message = str(e)
            listing_image.save()

    def queue_all_images(self, listing):
        """Queue all image types for generation"""
        prompts = self.create_image_prompts(listing)
        image_ids = []
        
        for image_type, prompt in prompts.items():
            # Create or update the image record
            listing_image, created = ListingImage.objects.update_or_create(
                listing=listing,
                image_type=image_type,
                defaults={
                    'prompt': prompt,
                    'status': 'pending'
                }
            )
            image_ids.append(listing_image.id)
            
            # Queue the image generation task
            if CELERY_AVAILABLE:
                generate_listing_image.delay(listing_image.id)
            else:
                # Generate synchronously if Celery is not available
                logger.warning("Celery not available - generating images synchronously")
                self.generate_image(listing_image.id)
        
        return image_ids


@shared_task
def generate_listing_image(listing_image_id):
    """Celery task to generate a single image"""
    service = ImageGenerationService()
    service.generate_image(listing_image_id)


@shared_task
def generate_all_listing_images(listing_id):
    """Celery task to generate all images for a listing"""
    from .models import GeneratedListing
    
    try:
        listing = GeneratedListing.objects.get(id=listing_id)
        service = ImageGenerationService()
        service.queue_all_images(listing)
    except GeneratedListing.DoesNotExist:
        logger.error(f"Listing {listing_id} not found")