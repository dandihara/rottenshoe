# Generated by Django 3.1.7 on 2022-01-07 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rottenshoe', '0004_auto_20220107_2151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sneakers',
            old_name='hot_score',
            new_name='score',
        ),
    ]
