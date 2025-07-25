# Generated manually for Product image field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_product_categories_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, help_text='Upload your product image', null=True, upload_to='products/'),
        ),
    ]