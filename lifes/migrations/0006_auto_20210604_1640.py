# Generated by Django 3.0.5 on 2021-06-04 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0005_remove_quantuser_serving'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='tag',
            field=models.CharField(choices=[('italian', 'italian'), ('chinese', 'chinese'), ('japanese', 'japanese'), ('indian', 'indian'), ('french', 'french'), ('american', 'american'), ('greek', 'greek'), ('spanish', 'spanish'), ('mediterranean', 'mediterranean'), ('lebanese', 'lebanese'), ('moroccan', 'moroccan'), ('turkish', 'turkish'), ('Thai', 'Thai'), ('Cajun', 'Cajun'), ('mexican', 'mexican'), ('caribbean', 'caribbean'), ('german', 'german'), ('russian', 'russian'), ('hungarian', 'hungarian')], default='indian', max_length=50),
        ),
        migrations.AddField(
            model_name='food',
            name='time_taken',
            field=models.CharField(default='10', max_length=10),
        ),
    ]
