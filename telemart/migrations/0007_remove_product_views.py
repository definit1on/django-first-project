# Generated by Django 4.1.1 on 2022-10-21 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telemart', '0006_company_official_product_hotline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='views',
        ),
    ]
