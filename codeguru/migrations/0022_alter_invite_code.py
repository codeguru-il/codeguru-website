# Generated by Django 3.2.11 on 2022-01-28 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0021_alter_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(
                default='WdfuUf9DHA9FvN4W42U2cdBmNt0rBIBFxJMCmRgOdTd0uqvqYgCMHOTu6oQUSJvl', max_length=64, unique=True),
        ),
    ]
