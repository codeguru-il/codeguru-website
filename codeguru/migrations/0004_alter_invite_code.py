# Generated by Django 5.1.2 on 2024-11-06 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0003_alter_cggroup_competition_alter_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(default='9DLD67oWBfvieYpycV4ksEJwiF6T2rsGsHSxnoxWaw687vDNxKyHxFhhBffiUlKO', max_length=64, unique=True),
        ),
    ]
