# Generated by Django 4.2.8 on 2024-02-11 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_remove_reportedproduct_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reportedproduct',
            old_name='product_id',
            new_name='id',
        ),
    ]