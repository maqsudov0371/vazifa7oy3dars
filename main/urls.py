from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="kirish"),
    path('verify-email/<str:code>/', VerifyEmailView.as_view(), name="verify_email"),
    path('contact/', ContactView.as_view(), name="contact"),
]
