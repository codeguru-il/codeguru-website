# Generated by Django 4.0.1 on 2022-01-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0015_alter_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(default='PbNzU7iAtAU062ME4z8dJxy7bEGvUCwmVuYwTOkSfzdZzWasEc18adcpJTwVhhkB', max_length=64, unique=True),
        ),
    ]
