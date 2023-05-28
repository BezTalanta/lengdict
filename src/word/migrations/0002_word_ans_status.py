# Generated by Django 4.1.4 on 2022-12-13 18:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='ans_status',
            field=models.SmallIntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(-10), django.core.validators.MaxValueValidator(10)], verbose_name='How many times user answer this right or wrong'),
        ),
    ]