# Generated by Django 3.0.5 on 2021-06-06 10:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0008_auto_20210605_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]