# Generated by Django 4.1.5 on 2023-02-01 03:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BeautyBarterAPI', '0005_remove_potentialbarter_member_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='potentialbarter',
            name='date_requested',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]