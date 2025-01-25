""" admin.py """
from django.contrib import admin
from .models import Donation, User

admin.site.register(User)
admin.site.register(Donation)
