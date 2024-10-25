from django.contrib import admin

# Register your models here.
from .models import Caisse,   Stock

admin.site.register(Caisse)
admin.site.register(Stock)