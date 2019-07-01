import calendar
from datetime import datetime, date
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.forms import model_to_dict
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import UpdateView

from VolleyUp.forms import *
from VolleyUp.utils import Calendar


class HomeView(View):

    def get(self, request):
        students = User.objects.all()
        context = {'students': students}
        return render(request, 'VolleyUp/home.html', context)


class RegisterUserView(View):

    def get(self, request):
        context = {'form': RegisterUserForm(),
                   'submit': 'Zarejestruj się'}
        return render(request, 'VolleyUp/form.html', context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            birth_date = form.cleaned_data.get('birth_date')
            sex = form.cleaned_data.get('sex')
            organization = form.cleaned_data.get('organization')
            level = form.cleaned_data.get('level')
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            User.objects.create_user(birth_date=birth_date, password=password, email=email, first_name=first_name,
                                     last_name=last_name, sex=sex, organization=organization, level=level,
                                     phone_number=phone_number)
            return redirect(reverse_lazy('login'))
        else:
            context = {'form': form,
                       'submit': 'Zarejestruj się'}
            return render(request, 'VolleyUp/form.html', context)


class EditUserView(View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(instance=user)
        context = {'form': form,
                   'submit': 'Zapisz zmiany'}
        return render(request, 'VolleyUp/form.html', context)

    def post(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('verify_user'))
        else:
            context = {'form': form,
                       'submit': 'Zapisz zmiany'}
            return render(request, 'VolleyUp/form.html', context)


class ChangePasswordView(View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        form = ChangePasswordForm()
        context = {'form': form,
                   'submit': 'Zmień hasło',
                   'user': user}
        return render(request, 'VolleyUp/form.html', context)

    def post(self, request, user_id):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            old_password = form.cleaned_data.get('old_password')
            check_user = authenticate(username=user, password=old_password)
            if check_user is not None:
                password = form.cleaned_data.get('password')
                user.set_password(password)
                user.save()
                return redirect('user_details', user_id=user_id)
            else:
                message = "Błędne stare hasło"
                context = {"form": form,
                           "submit": "Zaloguj",
                           "message": message}
                return render(request, "VolleyUp/form.html", context)
        else:
            context = {"form": form,
                       "submit": "dodaj użytkownika"}
            return render(request, "VolleyUp/form.html", context)


class LoginView(View):
    def get(self, request):
        context = {'form': LoginForm(),
                   'submit': 'Zaloguj się'}
        return render(request, 'VolleyUp/form.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get('user_email')
            user_password = form.cleaned_data.get('user_password')
            try:
                user_active = User.objects.get(email=user_email)
                if user_active.is_active is False:
                    context = {'form': LoginForm(),
                               'message': 'Musisz poczekać na weryfikację',
                               'submit': "Zaloguj się"}
                    return render(request, 'VolleyUp/form.html', context)
                user = authenticate(username=user_email, password=user_password)
                if user is not None:
                    login(request, user)
                    next = request.GET.get('next')
                    if next is not None:
                        return redirect(next)
                    return redirect(reverse_lazy('calendar'))
            except User.DoesNotExist:
                message = "Użytkownik o podanym adresie email nie istnieje, proszę się zarejestrować"
                context = {'form': form,
                           'submit': 'Zaloguj się',
                           'message': message}
                return render(request, 'VolleyUp/form.html', context)
        message = "Błędny email lub hasło"
        context = {'form': form,
                   'submit': 'Zaloguj się',
                   'message': message}
        return render(request, 'VolleyUp/form.html', context)
        # context = {'form': LoginForm(),
        #            'message': 'Musisz się zarejestrować lub poczekać na weryfikację',
        #            'submit': "Zaloguj się"}
        # return render(request, 'VolleyUp/form.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))


class AddTrainingView(View):

    def get(self, request):
        form = AddTrainingForm()
        context = {'form': form,
                   'submit': 'Dodaj trening'}
        return render(request, 'VolleyUp/form.html', context)

    def post(self, request):
        form = AddTrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('calendar'))
        context = {'form': form,
                   'submit': 'Dodaj trening'}
        return render(request, 'VolleyUp/form.html', context)


class EditTrainingView(View):

    def get(self, request, training_id):
        try:
            training = Training.objects.get(pk=training_id)
            form = AddTrainingForm(instance=training)
            context = {'form': form,
                       'submit': 'Zapisz trening',
                       'training': training}
        except Training.DoesNotExist:
            raise Http404('Taki trening nie istnieje')
        return render(request, 'VolleyUp/training.html', context)

    def post(self, request, training_id):
        action = request.POST.get('action')
        if action == 'Powiel trening':
            form = AddTrainingForm(request.POST)
            if form.is_valid():
                form.save()
        if action == 'Zapisz trening':
            training = Training.objects.get(pk=training_id)
            form = AddTrainingForm(request.POST, instance=training)
            if form.is_valid():
                form.save()
        if action == 'delete':
            training = Training.objects.get(pk=training_id)
            training.delete()
        return redirect(reverse_lazy('calendar'))


class VerifyUserView(View):

    def get(self, request):
        unverified_users = User.objects.filter(is_active=False)
        context = {'users': unverified_users}
        return render(request, 'VolleyUp/verify_user.html', context)

    def post(self, request):
        pk = request.POST.get('post_id')
        action = request.POST.get('action')
        user = User.objects.get(pk=pk)
        if action == 'verify':
            user.is_active = True
            user.save()
        else:
            deleted_user = f'{user.first_name} {user.last_name}'
            user.delete()
            unverified_users = User.objects.filter(is_active=False)
            context = {'message': "Usunięto użytkownika",
                       'users': unverified_users,
                       'deleted_user': deleted_user}
            return render(request, 'VolleyUp/verify_user.html', context)
        return redirect(reverse_lazy('verify_user'))


class CalendarView(generic.ListView):
    model = Training
    template_name = 'VolleyUp/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


class InfoView(View):

    def get(self, request):
        return render(request, 'VolleyUp/about.html')


class ContactView(View):

    def get(self, request):
        form = ContactForm()
        context = {'form': form,
                   'submit': 'Wyślij email'}
        return render(request, 'VolleyUp/contact.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            from_email = form.cleaned_data.get('from_email')
            message = form.cleaned_data.get('message')
            try:
                send_mail(subject, message, from_email, ['contact@volleyup.pl'])
            except BadHeaderError:
                return HttpResponse('Nieprawidłowy temat emaila')
            form = ContactForm()
            context = {'form': form,
                       'submit': 'Wyślij email',
                       'message': 'Dziękujemy za wysłanie emaila'}
            return render(request, 'VolleyUp/contact.html', context)
        form = ContactForm()
        context = {'form': form,
                   'submit': 'Wyślij email'}
        return render(request, 'VolleyUp/contact.html', context)


class RulesView(View):

    def get(self, request):
        return render(request, 'VolleyUp/rules.html')


class UserDetailsView(View):

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        context = {'user': user}
        return render(request, 'VolleyUp/user_details.html', context)
