from django.shortcuts import render
from .models import User
# Create your views here.
from rest_framework import generics
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny]) # On autorise tout le monde à voir l'accueil
def api_root(request):
    return Response({
        'status': 'success',
        'message': 'Bienvenue sur l\'API JobLink',
        'version': '1.0',
        'endpoints': {
            'register': 'http://127.0.0.1:8000/api/auth/register/',
            'login': 'http://127.0.0.1:8000/api/auth/login/',
            'token_refresh': 'http://127.0.0.1:8000/api/auth/token/refresh/',
        }
    })

class RegisterView(generics.CreateAPIView):
    # 1. Où chercher les données ?
    queryset = User.objects.all()
    
    # 2. Qui a le droit d'accéder à cette page ?
    # Ici "AllowAny" car tout le monde doit pouvoir s'inscrire, même sans badge.
    permission_classes = (AllowAny,) 
    
    # 3. Quel outil utiliser pour transformer le JSON en utilisateur ?
    # On lui donne le "mode d'emploi" que tu as créé dans serializers.py
    serializer_class = RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    # On spécifie que cette vue doit utiliser notre serializer personnalisé
    serializer_class = MyTokenObtainPairSerializer