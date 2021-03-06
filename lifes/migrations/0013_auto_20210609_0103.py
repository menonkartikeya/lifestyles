# Generated by Django 3.0.5 on 2021-06-08 19:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lifes', '0012_exlogs'),
    ]

    operations = [
        migrations.CreateModel(
            name='step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('step_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'User Steps',
            },
        ),
        migrations.AddField(
            model_name='bmi',
            name='bodyfat',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='exerciseplan',
            name='workoutday',
            field=models.CharField(default='Rest Day', max_length=100),
        ),
        migrations.AddField(
            model_name='myuser',
            name='fordiet',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='forfit',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='fornut',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='steps',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lifes.step'),
        ),
    ]
