import re
import phonenumbers
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Stock, Technicien
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


def indicatif():
    indicatifs = {}
    for region_code in phonenumbers.SUPPORTED_REGIONS:
        indicatif = phonenumbers.country_code_for_region(region_code)
        if indicatif:
            indicatifs[f'+{indicatif}'] = phonenumbers.region_code_for_country_code(indicatif)
    return [(key , f"{key} ({value})") for key , value in indicatifs.items()]
class TechnicienSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=True)
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(source = 'user.email', required = True)
    indicatif_telephone = serializers.ChoiceField(choices = indicatif(), required = True, write_only = True) 
    telephone = serializers.CharField(required = True)

    class Meta:
        model = Technicien
        fields = ['username', 'adresse', 'telephone', 'indicatif_telephone' ,'photo', 'email' , 'password']

        
    def validate(self,data):
        indicatif = data.pop ('indicatif_telephone')
        telephone = data.get ('telephone')

        try:
            number = f"{indicatif}{telephone}"
            parsed_number = phonenumbers.parse(number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number")
            data['telephone'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number")
        return data 
    
    def create(self, validated_data):
    # Extraire les données utilisateur
        user_data = validated_data.pop('user')
        username = user_data['username']
        email = user_data['email']
        password = validated_data.pop('password')

    # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error": "Ce nom d'utilisateur est déjà pris."})
    
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Cet email est déjà utilisé."})

    # Créer l'utilisateur
        user = User.objects.create_user(username=username, password=password, email=email)

        # Créer le technicien associé
        technicien = Technicien.objects.create(user=user, **validated_data)
    
        return technicien

    
    def validate_password(self, value):
        validate_password(value)
        return value
    
class TechnicienLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

#Inscription du client
class ClientSerializer(serializers.ModelSerializer):
    # Champs utilisateur
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, )

    # Champs spécifiques à Client
    adresse = serializers.CharField(required=True)
    telephone = serializers.CharField(required=True)

    class Meta:
        model = Client
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'adresse', 'telephone']

    def validate_password(self, value):
        # Vérifie la force du mot de passe
        validate_password(value)
        return value

    def create(self, validated_data):
        # Extraire les données utilisateur
        username = validated_data.pop('username')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error": "Ce nom d'utilisateur est déjà pris."})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Cet email est déjà utilisé."})

        # Créer l'utilisateur
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

        # Créer le client associé
        client = Client.objects.create(user=user, **validated_data)
        return client
    
#Connexion du client 
class ClientLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField( required=True, style={'input_type': 'password'})

    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        # Vérifier si l'identifier est un email ou un username
        if '@' in identifier:
            # Essayer de récupérer l'utilisateur par email
            try:
                user_obj = User.objects.get(email=identifier)
                # Utiliser le username pour l'authentification
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                raise AuthenticationFailed("Aucun utilisateur trouvé avec cet email.")
        else:
            # Authentification par username
            user = authenticate(username=identifier, password=password)

        if user is None:
            raise AuthenticationFailed("Nom d'utilisateur/email ou mot de passe incorrect.")

        if not user.is_active:
            raise AuthenticationFailed("Ce compte est désactivé.")

        # Si l'authentification réussit, ajouter l'utilisateur aux données validées
        data['user'] = user
        return data
    

class StockLoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Nom d'utilisateur")
    password = serializers.CharField(label="Mot de passe", style={'input_type': 'password'})

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # Authentifie l'utilisateur
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Nom d'utilisateur ou mot de passe incorrect.")

        # Vérifie si l'utilisateur est un gérant de stock
        if not hasattr(user, 'stock'):
            raise AuthenticationFailed("Vous n'êtes pas autorisé à accéder à cette ressource.")

        data['user'] = user
        return data