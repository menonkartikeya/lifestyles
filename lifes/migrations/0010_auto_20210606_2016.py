# Generated by Django 3.0.5 on 2021-06-06 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0009_auto_20210606_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantuser',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]