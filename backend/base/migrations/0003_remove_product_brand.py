# Generated by Django 3.2 on 2021-04-14 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
    ]
