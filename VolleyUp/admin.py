from django.contrib import admin

# Register your models here.
from VolleyUp.models import User, Training

admin.site.register(User)
admin.site.register(Training)