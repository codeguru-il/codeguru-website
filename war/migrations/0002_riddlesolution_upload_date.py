# Generated by Django 3.2.11 on 2022-01-24 19:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('war', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='riddlesolution',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
