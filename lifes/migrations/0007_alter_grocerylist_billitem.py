# Generated by Django 3.2.2 on 2021-05-17 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0006_myuser_allot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grocerylist',
            name='billitem',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lifes.bills'),
        ),
    ]
