# Generated by Django 4.2.11 on 2024-07-06 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_cart_checkout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='deleted',
        ),
    ]
