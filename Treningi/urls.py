"""Treningi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from VolleyUp.views import *

app_name = 'VolleyUp'
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register_user/$', RegisterUserView.as_view(), name='register_user'),
    url(r'^edit_user/(?P<user_id>(\d)+)/$', EditUserView.as_view(), name='edit_user'),
    url(r'^verify_user/$', VerifyUserView.as_view(), name='verify_user'),
    url(r'^add_training/$', AddTrainingView.as_view(), name='add_training'),
    url(r'^edit_training/(?P<training_id>(\d)+)/$', EditTrainingView.as_view(), name='edit_training'),
    url(r'^calendar/$', CalendarView.as_view(), name='calendar'),
    url(r'^about_facility/$', InfoView.as_view(), name='about'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^rules/$', RulesView.as_view(), name='rules'),
    url(r'^user_details/(?P<user_id>(\d)+)/$', UserDetailsView.as_view(), name='user_details'),
]

