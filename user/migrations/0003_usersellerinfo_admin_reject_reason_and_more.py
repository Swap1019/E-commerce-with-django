# Generated by Django 4.2.5 on 2023-11-06 18:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_usersellerinfo_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersellerinfo',
            name='admin_reject_reason',
            field=models.TextField(default='Not reviewed yet', help_text='Reject reason?'),
        ),
        migrations.AddField(
            model_name='usersellerinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usersellerinfo',
            name='review_status',
            field=models.CharField(choices=[('R', 'Reviewed'), ('N', 'Not reviewed')], default='N', max_length=1),
        ),
        migrations.AddField(
            model_name='usersellerinfo',
            name='user_description',
            field=models.TextField(blank=True, help_text='Any descriptions (optional)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_seller',
            field=models.CharField(choices=[('N', 'Not accepted'), ('I', 'Investigate'), ('A', 'Accepted')], default='I', max_length=1, verbose_name='seller'),
        ),
    ]