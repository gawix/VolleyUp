from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import RegexValidator
from django.utils import timezone

LEVELS = (

    (1, 'podstawowy'),
    (2, 'średniozaawansowany'),
    (3, 'profesjonalny'),

)

ORGANIZATIONS = (

    (1, 'PZU'),
    (2, 'Siemens'),
    (3, 'Wedel'),
    (4, 'PJATK'),
    (5, 'Volley Up'),

)

SEX = (

    (1, 'mężczyzna'),
    (2, 'kobieta'),

)

FACILITIES = (

    (1, 'Sala nr 1'),
    (2, 'Sala nr 2'),

)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    username = None
    email = models.EmailField('user email', unique=True)

    phone_number = models.CharField(verbose_name='numer telefonu', max_length=17)
    birth_date = models.IntegerField(verbose_name='data urodzenia', blank=True)
    sex = models.IntegerField(choices=SEX, default=1)
    organization = models.IntegerField(choices=ORGANIZATIONS, default=5)
    level = models.IntegerField(choices=LEVELS, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'birth_date', 'sex', 'organization', 'level']

    objects = UserManager()


TRAININGS = (

    (1, "PZU, poniedziałek, 20:30"),
    (2, "Volley Up, wtorek, 18:30"),
    (3, "Siemens, wtorek, 21:30"),
    (4, "Wedel, środa, 18:30"),
    (5, "PZU, środa, 20:00"),
    (6, "PJATK, środa, 21:30"),
    (7, "PJATK, czwartek, 18:30"),
    (8, "Volley Up, czwartek, 20:30"),

)


class Training(models.Model):
    start_time = models.IntegerField(choices=TRAININGS, default=1)
    facility = models.IntegerField(choices=FACILITIES, default=1)
    level = models.IntegerField(choices=LEVELS, default=1)
    organization = models.IntegerField(choices=ORGANIZATIONS, default=5)
    description = models.TextField(null=True)


