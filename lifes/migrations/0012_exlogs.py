# Generated by Django 3.0.5 on 2021-06-06 19:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0011_quantyrepssets'),
    ]

    operations = [
        migrations.CreateModel(
            name='exlogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('exercisename', models.ManyToManyField(related_name='Exercises', to='lifes.exercise')),
                ('us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Log Exercises!',
            },
        ),
    ]
