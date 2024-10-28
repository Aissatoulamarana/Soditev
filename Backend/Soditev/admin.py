from django.contrib import admin

# Register your models here.
from .models import Caisse,   Stock


admin.site.register(Stock)

#create caisse

# admin.py
from django.contrib import admin
from .models import Caisse
from django import forms

# admin.py
from django.contrib import admin
from .models import Caisse
from django import forms
from django.contrib.auth.models import User

# admin.py
from django.contrib import admin
from .models import Caisse
from django import forms
from django.contrib.auth.models import User

# admin.py
from django.contrib import admin
from .models import Caisse
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

# admin.py
from django.contrib import admin
from .models import Caisse
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from django import forms
from django.contrib.auth.models import User
from .models import Caisse

#creation d'un caissier
class CaisseForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Caisse
        fields = ('username', 'password')  # Ajoutez d'autres champs selon vos besoins

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        # Créer ou récupérer l'utilisateur
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save()

        # Créer l'instance de Caisse
        caisse = super().save(commit=False)
        caisse.caissier = user  # Associer l'utilisateur comme caissier
        if commit:
            caisse.save()
        return caisse

from django.contrib import admin
from .models import Caisse


@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    form = CaisseForm
    list_display = ('caissier','compte')  # Ajoutez une virgule pour indiquer que c'est un tuple
    search_fields = ('caissier__username',)  # Ajoutez une virgule pour indiquer que c'est un tuple
