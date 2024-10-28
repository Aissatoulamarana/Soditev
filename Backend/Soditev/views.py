from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from django.contrib.auth.models import User




from .serializers import ClientLoginSerializer, ClientSerializer, StockLoginSerializer,  TechnicienLoginSerializer, TechnicienSerializer

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
        serializer = ClientLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Générer ou récupérer le token pour l'utilisateur
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
class StockLoginView(GenericAPIView):
    serializer_class = StockLoginSerializer
    def post(self, request):
        serializer = StockLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Générer ou récupérer le token pour l'utilisateur
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)