# Generated by Django 3.0.5 on 2021-06-03 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0004_quantuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantuser',
            name='serving',
        ),
    ]