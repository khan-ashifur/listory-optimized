# Generated manually for ListingImage model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(choices=[('hero', 'Hero Shot'), ('infographic', 'Infographic'), ('lifestyle', 'Lifestyle'), ('testimonial', 'Testimonial'), ('whats_in_box', "What's in the Box")], max_length=20)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('generating', 'Generating'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('prompt', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('error_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='listings.generatedlisting')),
            ],
            options={
                'ordering': ['created_at'],
                'unique_together': {('listing', 'image_type')},
            },
        ),
    ]