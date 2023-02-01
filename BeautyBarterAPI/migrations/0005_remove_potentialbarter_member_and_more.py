# Generated by Django 4.1.5 on 2023-02-01 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BeautyBarterAPI', '0004_remove_service_admin_remove_service_member_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='potentialbarter',
            name='member',
        ),
        migrations.AddField(
            model_name='potentialbarter',
            name='member_requested',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_requested', to='BeautyBarterAPI.member'),
        ),
        migrations.AddField(
            model_name='potentialbarter',
            name='member_requesting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_requesting', to='BeautyBarterAPI.member'),
        ),
    ]
