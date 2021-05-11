# Generated by Django 3.2.2 on 2021-05-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0003_auto_20210511_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='name',
            field=models.CharField(default='food', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='stuff',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='foodplan',
            name='textrecipe',
            field=models.CharField(max_length=10000),
        ),
    ]
