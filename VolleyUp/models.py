from datetime import timedelta
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
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


class Organization(models.Model):
    name = models.IntegerField(choices=ORGANIZATIONS, default=5, verbose_name="Organizacja")

    # def __str__(self):
    #     return self.get_name_display()


class User(AbstractUser):

    username = None
    email = models.EmailField('user email', unique=True)

    phone_number = models.CharField(max_length=17)
    birth_date = models.IntegerField(blank=True)
    sex = models.IntegerField(choices=SEX, blank=True)
    level = models.IntegerField(choices=LEVELS, default=1)
    organization = models.ManyToManyField(Organization, verbose_name="Organizacja", related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'birth_date', 'sex', 'level']

    objects = UserManager()


class Training(models.Model):
    start_time = models.DateTimeField(default=timezone.now, verbose_name="Początek treningu")
    end_time = models.DateTimeField(default=lambda: timezone.now()+timedelta(hours=1.5), verbose_name="Koniec treningu")
    facility = models.IntegerField(choices=FACILITIES, default=1, verbose_name="Sala")
    level = models.IntegerField(choices=LEVELS, default=1, verbose_name="Poziom")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Organizacja")
    description = models.TextField(null=True, verbose_name="Opis treningu")

    class Meta:
        ordering = ('start_time',)

    @property
    def get_html_url(self):
        url = reverse('edit_training', args=(self.id,))
        local_start_time = timezone.localtime(self.start_time)
        local_end_time = local_start_time + timedelta(hours=1.5)
        return f'<a href="{url}">{self.organization.get_name_display()}, ' \
               f'{local_start_time.strftime("%H:%M")} - {local_end_time.strftime("%H:%M")} </a>'
