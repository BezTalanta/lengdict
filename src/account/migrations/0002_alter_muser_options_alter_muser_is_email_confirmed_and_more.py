# Generated by Django 4.1.4 on 2022-12-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='muser',
            options={'ordering': ['is_user_premium'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AlterField(
            model_name='muser',
            name='is_email_confirmed',
            field=models.BooleanField(default=False, verbose_name='Have user confirmed email'),
        ),
        migrations.AlterField(
            model_name='muser',
            name='is_user_premium',
            field=models.BooleanField(default=False, verbose_name='Does user has premium'),
        ),
    ]
