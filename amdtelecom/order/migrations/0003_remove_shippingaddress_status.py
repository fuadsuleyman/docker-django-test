# Generated by Django 3.1.4 on 2021-02-26 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20210226_0402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippingaddress',
            name='status',
        ),
    ]