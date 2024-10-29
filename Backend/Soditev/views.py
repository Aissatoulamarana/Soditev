
from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from .serializers import ClientLoginSerializer, ClientSerializer, CommerciauxLoginSerializer, CommerciauxSerializer, LoginCaissierSerializer, StockLoginSerializer,  TechnicienLoginSerializer, TechnicienSerializer

class InscriptionTechnicienView(generics.CreateAPIView):
    serializer_class = TechnicienSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class TechnicienLoginView(GenericAPIView):
    serializer_class = TechnicienLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Vérifie que l'utilisateur est un technicien
            if hasattr(user, 'technicien'):
                # Vérification du statut du technicien
                if user.technicien.statut == 'ACTIF':
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({"token": token.key}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Votre compte est inactif"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "Vous n'êtes pas un technicien"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
class ClientRegistrationView(GenericAPIView):
    serializer_class = ClientSerializer
    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        
        # Vérifier la validité des données
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Client inscrit avec succès"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientLoginView(GenericAPIView):
    serializer_class = ClientLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            # Vérifie que l'utilisateur est un client
            if hasattr(user, 'client'):  # Assurez-vous que l'utilisateur a un attribut 'client'
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Vous n'êtes pas un client"}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
    
class StockLoginView(GenericAPIView):
    serializer_class = StockLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Authentification de l'utilisateur
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # Vérifie que l'utilisateur est un membre du stock
            if hasattr(user, 'stock'):  # Assurez-vous que l'utilisateur a un attribut 'stock'
                # Générer ou récupérer le token pour l'utilisateur
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Vous n'êtes pas un membre du stock"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
    

#Vue pour afficher la page principale
def HomeView(request):
    return render(request, 'index.html')# Fichier HTML principal généré par React




class RegistrationView(GenericAPIView):
    serializer_class = CommerciauxSerializer
    def post(self, request):
        serializer = CommerciauxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Inscription réussie"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#view pour la connexion des commerciaux
class CommerciauxLoginView(GenericAPIView):
    serializer_class = CommerciauxLoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            #verifier que l'utilisateur est un technicien
            if hasattr(user, 'commerciaux'):
                #verifier le statut du commerciaux
                if user.commerciaux.statut == 'ACTIF':
                    token, create = Token.objects.get_or_create(user=user)
                    return Response({"token":token.key}, status=statut.HTTP_200_OK)
                else:
                    return Response({"error": "Votre compte est inactif"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error ": "Vous n'êtes pas un Commerciaux"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error ": "Nom d'utilisateur ou Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
    

#view caissier


class LoginCaissierView(GenericAPIView):
    serializer_class = LoginCaissierSerializer
    def post(self, request):
        serializer = LoginCaissierSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Vous pouvez ajouter un token ou d'autres informations à la réponse si nécessaire
            return Response({"message": "Connexion réussie", "username": user.username}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegistrationView(GenericAPIView):
    serializer_class = CommerciauxSerializer
    def post(self, request):
        serializer = CommerciauxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Inscription réussie"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#view pour la connexion des commerciaux
class CommerciauxLoginView(GenericAPIView):
    serializer_class = CommerciauxLoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            #verifier que l'utilisateur est un technicien
            if hasattr(user, 'commerciaux'):
                #verifier le statut du commerciaux
                if user.commerciaux.statut == 'ACTIF':
                    token, create = Token.objects.get_or_create(user=user)
                    return Response({"token":token.key}, status=statut.HTTP_200_OK)
                else:
                    return Response({"error": "Votre compte est inactif"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error ": "Vous n'êtes pas un Commerciaux"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error ": "Nom d'utilisateur ou Mot de passe incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
    

#view caissier


class LoginCaissierView(GenericAPIView):
    serializer_class = LoginCaissierSerializer
    def post(self, request):
        serializer = LoginCaissierSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Vous pouvez ajouter un token ou d'autres informations à la réponse si nécessaire
            return Response({"message": "Connexion réussie", "username": user.username}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


