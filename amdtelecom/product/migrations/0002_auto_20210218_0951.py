# Generated by Django 3.1.4 on 2021-02-18 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marka',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=110, unique=True, verbose_name='Slug'),
        ),
    ]
