# Generated by Django 5.1.2 on 2024-11-07 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0005_alter_cggroup_competition_alter_invite_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(default='4NuMTEGZjhskYAowyRPcpxQhi4LKUNO7gxUT3oKpSM4dsFXm3mrFlqxEJ1GByxUV', max_length=64, unique=True),
        ),
    ]
