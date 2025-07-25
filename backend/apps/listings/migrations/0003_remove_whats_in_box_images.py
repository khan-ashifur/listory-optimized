# Remove what's in the box image type

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_listingimage'),
    ]

    operations = [
        # Remove any existing what's in the box images
        migrations.RunSQL(
            "DELETE FROM listings_listingimage WHERE image_type = 'whats_in_box';",
            reverse_sql="-- No reverse operation needed"
        ),
    ]