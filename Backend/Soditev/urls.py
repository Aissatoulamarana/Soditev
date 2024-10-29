from django.urls import path
from . views import ClientLoginView, ClientRegistrationView, InscriptionTechnicienView, StockLoginView, TechnicienLoginView
from . import views


urlpatterns = [
    path('inscription/', InscriptionTechnicienView.as_view(), name='inscription_technicien'),#Inscription des tehniciens 
    path('connexion/', TechnicienLoginView.as_view(), name= 'connexion-tech'),#Connexion des techniciens 
    path('inscription-client/', ClientRegistrationView.as_view(), name='inscription-client'),#inscription des clients
    path('connexion-client/', ClientLoginView.as_view(), name= 'connexion_client'),#Connexion des clients
    path('connexion-g_stock/',StockLoginView.as_view(), name= 'connexion_g-stock'),# connexion des gérants de stock
    path('', views.HomeView, name='home'),  # Page d'accueil

]
