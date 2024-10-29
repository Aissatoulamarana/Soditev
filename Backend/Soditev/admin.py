from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
import phonenumbers
from django.contrib.auth.password_validation import validate_password

# Register your models here.
from .models import Caisse, Client,   Stock, Technicien


admin.site.register(Caisse)


class TechnicienAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'telephone','user__email', 'statut', 'disponibilite')  # Affiche ces champs dans la liste
    list_filter = ('statut',)  # Ajoute un filtre pour le statut
    search_fields = ('user__username', 'adresse', 'telephone')  # Ajoute une barre de recherche
    actions = ['activer_techniciens', 'desactiver_techniciens']  # Ajoute des actions pour activer/désactiver

    # Actions pour activer et désactiver les techniciens
    @admin.action(description="Activer les techniciens sélectionnés")
    def activer_techniciens(self, request, queryset):
        queryset.update(statut='ACTIF')

    @admin.action(description="Désactiver les techniciens sélectionnés")
    def desactiver_techniciens(self, request, queryset):
        queryset.update(statut='NON_ACTIF')

admin.site.register(Technicien, TechnicienAdmin)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'adresse', 'telephone', 'user__email')
    ordering = ('-user',)

class StockAdminForm(forms.ModelForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=150, help_text="Doit être unique.")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, help_text="Le mot de passe doit être fort.")

    class Meta:
        model = Stock
        fields = [ 'username',  'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean_telephone(self):
        indicatif = self.cleaned_data.get("indicatif", "+221")
        telephone = self.cleaned_data['telephone']
        full_number = f"{indicatif}{telephone}"
        
        try:
            parsed_phone = phonenumbers.parse(full_number, None)
            if not phonenumbers.is_valid_number(parsed_phone):
                raise forms.ValidationError("Numéro de téléphone invalide.")
            # Retourne le numéro formaté (internationale)
            return phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Numéro de téléphone invalide.")

    def save(self, commit=True):
        username = self.cleaned_data.pop('username')
        password = self.cleaned_data.pop('password')

        user = User.objects.create_user(username=username,  password=password)

        stock = super().save(commit=False)
        stock.gerant = user

        if commit:
            stock.save()
        return stock

# Configuration de l’administration pour utiliser le formulaire personnalisé
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    form = StockAdminForm
    list_display = ('gerant', )
    search_fields = ('gerant__username', )


admin.site.register(Stock)



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




@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    form = CaisseForm
    list_display = ('caissier','compte')  # Ajoutez une virgule pour indiquer que c'est un tuple
    search_fields = ('caissier__username',)  # Ajoutez une virgule pour indiquer que c'est un tuple

