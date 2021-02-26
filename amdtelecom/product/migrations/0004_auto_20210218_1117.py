# Generated by Django 3.1.4 on 2021-02-18 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210218_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='marka',
        ),
        migrations.AddField(
            model_name='product',
            name='marka',
            field=models.ManyToManyField(related_name='marka', to='product.Marka'),
        ),
    ]
