""" admin.py """
from django.contrib import admin
from .models import Donation, DropOffsite, Proof, Receipt, User

admin.site.register(User)
admin.site.register(Donation)
admin.site.register(Proof)
admin.site.register(DropOffsite)
admin.site.register(Receipt)
