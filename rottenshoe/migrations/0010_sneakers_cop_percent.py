# Generated by Django 4.0.1 on 2022-01-16 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rottenshoe', '0009_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='sneakers',
            name='cop_percent',
            field=models.FloatField(default=0),
        ),
    ]
