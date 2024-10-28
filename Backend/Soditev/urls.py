from django.urls import path
from . views import ClientLoginView, ClientRegistrationView, InscriptionTechnicienView, StockLoginView, TechnicienLoginView


urlpatterns = [
    path('inscription/', InscriptionTechnicienView.as_view(), name='inscription_technicien'),
    path('connexion/', TechnicienLoginView.as_view(), name= 'connexion-tech'),
    path('inscription-client/', ClientRegistrationView.as_view(), name='inscription-client'),
    path('connexion-client/', ClientLoginView.as_view(), name= 'connexion_client'),
    path('connexion-g_stock/',StockLoginView.as_view(), name= 'connexion_g-stock')
]
