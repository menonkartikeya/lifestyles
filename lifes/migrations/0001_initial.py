# Generated by Django 3.0.5 on 2021-05-22 13:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], max_length=50, null=True)),
                ('mobno', models.BigIntegerField(default=0)),
                ('height', models.FloatField(blank=True, default=0.0)),
                ('weight', models.FloatField(blank=True, default=0.0)),
                ('target', models.CharField(blank=True, choices=[('Gain Weight', 'Gain Weight'), ('Stay Fit', 'Stay Fit'), ('Loose Weight', 'Loose Weight')], max_length=60, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('allotnutri', models.BooleanField(default=False)),
                ('allotdieti', models.BooleanField(default=False)),
                ('allottrain', models.BooleanField(default=False)),
                ('bio', models.CharField(max_length=5000)),
                ('location', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'User Details!',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='bills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoicepdf', models.FileField(blank=True, null=True, upload_to='')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Manage Bills!',
            },
        ),
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('mobno', models.BigIntegerField(default=0)),
                ('bookcall', models.BooleanField(blank=True, null=True)),
                ('bookapp', models.BooleanField(blank=True, null=True)),
                ('message', models.CharField(max_length=500)),
                ('check', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Check Contact Entries!',
            },
        ),
        migrations.CreateModel(
            name='dietplan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remarks', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Manage Diet Plans Issued!',
            },
        ),
        migrations.CreateModel(
            name='food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.URLField()),
                ('name', models.CharField(max_length=100)),
                ('stuff', models.CharField(max_length=10000)),
                ('calories', models.IntegerField(default=0)),
                ('protein', models.IntegerField(default=0)),
                ('fat', models.IntegerField(default=0)),
                ('carbs', models.IntegerField(default=0)),
                ('fiber', models.IntegerField(default=0)),
                ('unit', models.CharField(choices=[('piece', 'piece'), ('slice', 'slice'), ('Katori', 'Katori'), ('g', 'g'), ('oz', 'oz'), ('cup', 'cup'), ('serving', 'serving'), ('mg', 'mg')], max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Manage Food Items!',
            },
        ),
        migrations.CreateModel(
            name='live',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slottime', models.TimeField()),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Check Live Meetings!',
            },
        ),
        migrations.CreateModel(
            name='logger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Log Meals!',
            },
        ),
        migrations.CreateModel(
            name='streak',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('days', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Streaks!',
            },
        ),
        migrations.CreateModel(
            name='subplans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('Free Plan', 'Free Plan'), ('Basic Plan', 'Basic Plan'), ('Premium Plan', 'Premium Plan')], max_length=100)),
                ('price', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Subscription Plans!',
            },
        ),
        migrations.CreateModel(
            name='foodplan',
            fields=[
                ('textrecipe', models.CharField(max_length=10000)),
                ('fooditem', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='lifes.food')),
            ],
            options={
                'verbose_name_plural': 'Manage Food Plans!',
            },
        ),
        migrations.CreateModel(
            name='bmr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bmr', models.FloatField(default=0.0)),
                ('date', models.DateField(auto_now_add=True)),
                ('maintcalo', models.IntegerField(default=0)),
                ('us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'BMR INDEX',
            },
        ),
        migrations.CreateModel(
            name='bmi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bmi', models.FloatField(default=0.0)),
                ('date', models.DateField(auto_now_add=True)),
                ('us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'BMI INDEX',
            },
        ),
        migrations.AddField(
            model_name='myuser',
            name='bill',
            field=models.ManyToManyField(blank=True, to='lifes.bills'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='diets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lifes.dietplan'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='lives',
            field=models.ManyToManyField(blank=True, to='lifes.live'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='log',
            field=models.ManyToManyField(blank=True, to='lifes.logger'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='streaks',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lifes.streak'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='sub',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lifes.subplans'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='logger',
            name='dinner',
            field=models.ManyToManyField(blank=True, related_name='dinner', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='logger',
            name='extra',
            field=models.ManyToManyField(blank=True, related_name='Extra', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='logger',
            name='lunch',
            field=models.ManyToManyField(blank=True, related_name='lunch', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='logger',
            name='postworkout',
            field=models.ManyToManyField(blank=True, related_name='Post_work', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='logger',
            name='preworkout',
            field=models.ManyToManyField(blank=True, related_name='Pre_work', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='logger',
            name='snacks',
            field=models.ManyToManyField(blank=True, related_name='snack', to='lifes.foodplan'),
        ),
        migrations.CreateModel(
            name='grocerylist',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('billitem', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='lifes.bills')),
                ('items', models.ManyToManyField(blank=True, to='lifes.food')),
            ],
            options={
                'verbose_name_plural': 'Current Grocery Lists!',
            },
        ),
        migrations.CreateModel(
            name='employeecontrol',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mobno', models.BigIntegerField()),
                ('employeetype', models.CharField(choices=[('Nutritionist', 'Nutritionist'), ('Dietician', 'Dietician'), ('employee', 'employee'), ('Fitness Trainer', 'Fitness Trainer'), ('finance', 'finance')], max_length=100)),
                ('certificate', models.URLField()),
                ('resume', models.URLField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], max_length=50)),
                ('alloted', models.ManyToManyField(blank=True, related_name='Alloted_Users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Check Employees!',
            },
        ),
        migrations.AddField(
            model_name='dietplan',
            name='dinner',
            field=models.ManyToManyField(related_name='Dinner', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='dietplan',
            name='lunch',
            field=models.ManyToManyField(related_name='Lunch', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='dietplan',
            name='postworkout',
            field=models.ManyToManyField(related_name='Post_Workout', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='dietplan',
            name='preworkout',
            field=models.ManyToManyField(related_name='Pre_Workout', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='dietplan',
            name='snacks',
            field=models.ManyToManyField(related_name='Snacks', to='lifes.foodplan'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='foodplans',
            field=models.ManyToManyField(blank=True, to='lifes.foodplan'),
        ),
    ]
