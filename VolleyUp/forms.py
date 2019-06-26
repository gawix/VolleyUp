from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import PasswordInput

from VolleyUp.models import *


def validate_email(value):
    if User.objects.filter(email=value):
        raise ValidationError("Email: {} jest już zajęty".format(value))


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=64, label="Imię")
    last_name = forms.CharField(max_length=128, label="Nazwisko")
    birth_date = forms.IntegerField(min_value=1940, max_value=2005, label="Rok urodzenia")
    sex = forms.ChoiceField(choices=SEX, label="Płeć")
    organization = forms.ChoiceField(choices=ORGANIZATIONS, label="Organizacja")
    level = forms.ChoiceField(choices=LEVELS, label="Jak oceniasz swój poziom umiejętności")
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', label="Numer telefonu",
                                    error_messages={'invalid': "Numer telefonu musi zawierać między 9-15 cyfr"})
    email = forms.EmailField(validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(), label="Podaj hasło")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Potwierdź hasło")

    def clean_password_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        print(password, confirm_password)
        if password != confirm_password:
            raise forms.ValidationError(
                "Wprowadź dwa razy to samo hasło"
            )
        return password


class LoginForm(forms.Form):
    user_email = forms.EmailField(label="Podaj email")
    user_password = forms.CharField(widget=PasswordInput(), label="Podaj hasło")


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'

