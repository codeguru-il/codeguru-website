# Generated by Django 4.0.1 on 2022-01-31 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0026_alter_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(default='xhlg3J8DWpZx1IsWhEPLhQ9BFSIdmH8D0uNeEI9Br1n0HPKm5cUILbdWFD7vY54f', max_length=64, unique=True),
        ),
    ]
