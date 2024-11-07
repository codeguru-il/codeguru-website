# Generated by Django 5.1.2 on 2024-11-07 16:20

import django.core.validators
import war.models
import war.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0006_alter_invite_code'),
        ('war', '0002_alter_riddle_competition_alter_war_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riddlesolution',
            name='riddle_solution',
            field=models.FileField(storage=war.storage.submissions_storage, upload_to=war.models.riddle_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['zip'])]),
        ),
        migrations.AlterField(
            model_name='survivor',
            name='asm_file',
            field=models.FileField(null=True, storage=war.storage.submissions_storage, upload_to=war.models.asm_surv_upload, validators=[war.models.asm_max]),
        ),
        migrations.AlterField(
            model_name='survivor',
            name='bin_file',
            field=models.FileField(storage=war.storage.submissions_storage, upload_to=war.models.bin_surv_upload, validators=[war.models.bin_max]),
        ),
        migrations.AlterField(
            model_name='survivor',
            name='result',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddConstraint(
            model_name='survivor',
            constraint=models.CheckConstraint(condition=models.Q(('result__gte', 0.0)), name='positive_result'),
        ),
    ]