from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from VolleyUp.models import *
from django.views import View
from VolleyUp.forms import *


class HomeView(View):

    def get(self, request):
        students = User.objects.all()
        context = {'students': students}
        return render(request, 'VolleyUp/home.html', context)


class AddUserView(View):

    def get(self, request):
        form = AddUserForm()
        context = {'form': form,
                   'submit': 'Dodaj studenta'}
        return render(request, 'VolleyUp/form.html', context)

    def post(self, request):
        form = AddUserForm(request.POST)

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
            return redirect(reverse_lazy('home'))
        else:
            context = {'form': form,
                       'submit': 'Dodaj studenta'}
            return render(request, 'VolleyUp/form.html', context)


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
            user = authenticate(username=user_email, password=user_password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next')
                if next is not None:
                    return redirect(next)
                return redirect(reverse_lazy('home'))

        context = {'form': LoginForm(),
                   'message': 'Musisz poczekać na weryfikację',
                   'submit': "Zaloguj się"}
        return render(request, 'VolleyUp/form.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('home'))


class AddTrainingView(View):

    def get(self, request):
        form = AddTrainingForm()
        context = {'form': form,
                   'submit': 'Dodaj trening'}
        return render(request, 'VolleyUp/add_training.html', context)

    def post(self, request):
        form = AddTrainingForm(request.POST)
        if form.is_valid():
            start_time = form.cleaned_data.get('start_time')
            facility = form.cleaned_data.get('facility')
            level = form.cleaned_data.get('level')
            organization = form.cleaned_data.get('organization')
            description = form.cleaned_data.get('description')
            Training.objects.create(start_time=start_time, facility=facility, level=level, organization=organization,
                                    description=description)
            return redirect(reverse_lazy('home'))
        else:
            context = {'form': form,
                       'submit': 'Dodaj trening'}
            return render(request, 'VolleyUp/add_training.html', context)


class VerifyUserView(View):

    def get(self, request):
        unverified_users = User.objects.filter(is_active=False)
        context = {'users': unverified_users}
        return render(request, 'VolleyUp/verify_user.html', context)

    def post(self, request):
        pk = request.POST.get('post_id')
        user = User.objects.get(pk=pk)
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('verify_user'))
