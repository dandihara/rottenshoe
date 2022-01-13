# Generated by Django 3.1.7 on 2022-01-07 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rottenshoe', '0003_auto_20211210_1818'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sneakers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sneaker_name', models.CharField(max_length=200)),
                ('model_number', models.CharField(max_length=30)),
                ('brand', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('hot_score', models.FloatField(default=0.0)),
                ('thumbnail', models.ImageField(blank=True, upload_to='images/')),
                ('retail_date', models.DateField()),
            ],
            options={
                'db_table': 'sneakers',
            },
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comments',
        ),
        migrations.AlterModelTable(
            name='scoreboard',
            table='sneakers_score',
        ),
        migrations.AlterModelTable(
            name='user',
            table='User',
        ),
        migrations.AlterField(
            model_name='comment',
            name='board_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rottenshoe.sneakers'),
        ),
        migrations.AlterField(
            model_name='scoreboard',
            name='board_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rottenshoe.sneakers'),
        ),
        migrations.DeleteModel(
            name='SneakerBoard',
        ),
    ]