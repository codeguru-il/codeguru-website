# Generated by Django 4.0.1 on 2022-02-01 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeguru', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(default='wddy60kUW5YGtBC6TwUQBLypboB50EsrZJdKGExaW4tmtXO5rGhzSTs9wAA5W9zL', max_length=64, unique=True),
        ),
    ]
