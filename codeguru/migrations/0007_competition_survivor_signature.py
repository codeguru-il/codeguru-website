# Generated by Django 5.1.3 on 2024-11-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0006_alter_invite_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='survivor_signature_enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='competition',
            name='survivor_signature_gap',
            field=models.PositiveIntegerField(default=49),
        ),
        migrations.AddField(
            model_name='competition',
            name='survivor_signature_offset',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='competition',
            name='survivor_signature_value',
            field=models.BinaryField(default=b'\x90', max_length=1),
        ),
    ]
