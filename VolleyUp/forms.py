from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import PasswordInput, DateInput
from django.utils.safestring import mark_safe
from VolleyUp.models import *


def validate_email(value):
    if User.objects.filter(email=value):
        raise ValidationError("Email: {} jest już zajęty".format(value))


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(max_length=64, label="Imię")
    last_name = forms.CharField(max_length=128, label="Nazwisko")
    birth_date = forms.IntegerField(min_value=1930, max_value=2005, label="Rok urodzenia")
    sex = forms.ChoiceField(choices=SEX, label="Płeć")
    organization = forms.ChoiceField(choices=ORGANIZATIONS, label="Organizacja")
    level = forms.ChoiceField(choices=LEVELS, label=mark_safe("Jak oceniasz swój <br /> poziom umiejętności"))
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$', label="Numer telefonu",
                                    error_messages={'invalid': "Numer telefonu musi zawierać między 9-15 cyfr"})
    email = forms.EmailField(validators=[validate_email])
    password = forms.CharField(widget=forms.PasswordInput(), label="Podaj hasło")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Potwierdź hasło")

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "Wprowadź dwa razy to samo hasło"
            )
        return password


class EditUserForm(UserChangeForm):

    password = None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'sex', 'organization', 'level']
        labels = {'email': 'Email', 'phone_number': 'Numer telefonu', 'birth_date': 'Rok urodzenia', 'sex': 'Płeć',
                  'organization': 'Organizacja', 'level': 'Poziom'}


class LoginForm(forms.Form):
    user_email = forms.EmailField(label="Podaj email")
    user_password = forms.CharField(widget=PasswordInput(), label="Podaj hasło")


class AddTrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = '__all__'
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super(AddTrainingForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%d %H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%d %H:%M',)


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label='Podaj swój email')
    subject = forms.CharField(required=True, max_length=256, label='Temat')
    message = forms.CharField(required=True, widget=forms.Textarea, label=mark_safe('Treść <br />wiadomości'))