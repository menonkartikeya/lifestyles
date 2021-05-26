# Generated by Django 3.0.5 on 2021-05-26 20:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0007_requestchange'),
    ]

    operations = [
        migrations.AddField(
            model_name='bills',
            name='billtype',
            field=models.CharField(choices=[('subscriptions', 'subscriptions'), ('grocery', 'grocery'), ('products', 'products'), ('Other', 'Other')], default='Other', max_length=1000),
        ),
        migrations.AddField(
            model_name='bills',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bills',
            name='expiry',
            field=models.BooleanField(default=False),
        ),
    ]