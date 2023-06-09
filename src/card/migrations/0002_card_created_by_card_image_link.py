# Generated by Django 4.1.4 on 2022-12-30 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Who has created this card'),
        ),
        migrations.AddField(
            model_name='card',
            name='image_link',
            field=models.ImageField(default='not_found.png', upload_to='card_images/', verbose_name="Card's image"),
        ),
    ]
