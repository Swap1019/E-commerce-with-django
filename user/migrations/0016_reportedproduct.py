# Generated by Django 4.2.8 on 2024-02-02 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_rename_taggings_theproduct_tags'),
        ('user', '0015_remove_user_admin_reject_reason'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('1', 'NSFW'), ('2', 'Fake Product'), ('3', 'Scam')], max_length=1)),
                ('explanation', models.TextField()),
                ('reported_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.theproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id')),
            ],
        ),
    ]
