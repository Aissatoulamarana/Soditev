#Fichier serializer

from rest_framework import generics, permissions,serializers
from .models import Commerciaux

from django.contrib.auth.hashers import make_password


from django.contrib.auth.models import UserManager

from django.contrib.auth.models import User

import re
from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token




from rest_framework import serializers
from django.contrib.auth.models import User

from django_countries.fields import CountryField
from django_countries.serializers import CountryFieldMixin



import phonenumbers
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Commerciaux
from django.contrib.auth import authenticate

from django.contrib import admin
from .models import Caisse

# Fonction pour récupérer les indicatifs téléphoniques
def obtenir_indicatifs_telephoniques():
    indicatifs = {}
    for region_code in phonenumbers.SUPPORTED_REGIONS:
        indicatif = phonenumbers.country_code_for_region(region_code)
        if indicatif:
            indicatifs[f"+{indicatif}"] = phonenumbers.region_code_for_country_code(indicatif)
    return [(key, f"{key} ({value})") for key, value in indicatifs.items()]

class CommerciauxSerializer(serializers.ModelSerializer): 
    username = serializers.CharField(source='user.username', required=True)
    adresse = serializers.CharField(required=True)
    email = serializers.EmailField(source='user.email', required=True)
    indicatif_telephone = serializers.ChoiceField(choices=obtenir_indicatifs_telephoniques(), required=True,write_only=True)
    telephone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Commerciaux
        fields = ('id', 'username', 'adresse', 'email', 'telephone', 'indicatif_telephone', 'photo', 'password')

    def validate_password(self, value):
        if not re.search(r'[A-Za-z]', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins une lettre.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
        if len(value) < 8:
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return value

    def validate_telephone(self, value):
        # Vérifier que le téléphone contient uniquement des chiffres
        if not re.fullmatch(r'\d+', value):
            raise serializers.ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
        return value

    def validate(self, data):
        # Récupérer l'indicatif et le numéro de téléphone
        indicatif = data.pop('indicatif_telephone')
        telephone = data.get('telephone')
        
        # Utiliser `phonenumbers` pour valider et formater le numéro complet
        try:
            numero_complet = f"{indicatif}{telephone}"
            parsed_number = phonenumbers.parse(numero_complet, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Le numéro de téléphone n'est pas valide pour l'indicatif sélectionné.")
            # Formater le numéro en version internationale
            data['telephone'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Le format du numéro de téléphone est incorrect.")
        
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        
        # Créer l'utilisateur
        user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=password)
        
        # Associer l'utilisateur au `Commerciaux`
        commerciaux = Commerciaux.objects.create(user=user, **validated_data)
        
        return commerciaux
    #connexion commerciaux
class CommerciauxLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
        
#connexion des caissiers 



class LoginCaissierSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Nom d'utilisateur ou mot de passe incorrect.")
        data['user'] = user
        return data





