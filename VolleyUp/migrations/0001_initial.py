# Generated by Django 2.2.2 on 2019-07-01 19:07

import VolleyUp.models
import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(choices=[(1, 'PZU'), (2, 'Siemens'), (3, 'Wedel'), (4, 'PJATK'), (5, 'Volley Up')], default=5)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='user email')),
                ('phone_number', models.CharField(max_length=17)),
                ('birth_date', models.IntegerField(blank=True)),
                ('sex', models.IntegerField(blank=True, choices=[(1, 'mężczyzna'), (2, 'kobieta')])),
                ('level', models.IntegerField(choices=[(1, 'podstawowy'), (2, 'średniozaawansowany'), (3, 'profesjonalny')], default=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('organization', models.ManyToManyField(to='VolleyUp.Organization', verbose_name='Organizacja')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', VolleyUp.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Początek treningu')),
                ('end_time', models.DateTimeField(default=datetime.datetime(2019, 7, 1, 20, 37, 45, 252503, tzinfo=utc), verbose_name='Koniec treningu')),
                ('facility', models.IntegerField(choices=[(1, 'Sala nr 1'), (2, 'Sala nr 2')], default=1, verbose_name='Sala')),
                ('level', models.IntegerField(choices=[(1, 'podstawowy'), (2, 'średniozaawansowany'), (3, 'profesjonalny')], default=1, verbose_name='Poziom')),
                ('description', models.TextField(null=True, verbose_name='Opis treningu')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VolleyUp.Organization')),
            ],
            options={
                'ordering': ('start_time',),
            },
        ),
    ]
