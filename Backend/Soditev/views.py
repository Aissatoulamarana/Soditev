from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CommerciauxSerializer , CommerciauxLoginSerializer, LoginCaissierSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status

from rest_framework.permissions import IsAuthenticated


from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny



from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


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

