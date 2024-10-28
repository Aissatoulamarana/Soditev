
from django.urls import path
from .views import CommerciauxLoginView, LoginCaissierView, RegistrationView
urlpatterns = [
 path('register/', RegistrationView.as_view(), name='register'),
 path('login/', CommerciauxLoginView.as_view(), name='login'),
 path('loginCaissier/', LoginCaissierView.as_view(), name='loginCaissier'),
]