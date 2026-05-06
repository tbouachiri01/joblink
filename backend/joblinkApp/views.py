from django.shortcuts import render
from .models import User
from rest_framework import generics
from .serializers import RegisterSerializer, MyTokenObtainPairSerializer, ProfilCandidatSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import ProfilCandidat

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'status': 'success',
        'message': 'Bienvenue sur l\'API JobLink',
        'version': '1.0',
        'endpoints': {
            'register': 'http://127.0.0.1:8000/api/auth/register/',
            'login': 'http://127.0.0.1:8000/api/auth/login/',
            'token_refresh': 'http://127.0.0.1:8000/api/auth/token/refresh/',
            'profil': 'http://127.0.0.1:8000/api/profil/',
        }
    })

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProfilCandidatView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        try:
            profil = ProfilCandidat.objects.get(user=request.user)
            return Response(ProfilCandidatSerializer(profil).data)
        except ProfilCandidat.DoesNotExist:
            return Response({'detail': 'Profil non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if ProfilCandidat.objects.filter(user=request.user).exists():
            return Response({'detail': 'Profil déjà existant.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfilCandidatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profil = ProfilCandidat.objects.get(user=request.user)
        except ProfilCandidat.DoesNotExist:
            return Response({'detail': 'Profil non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfilCandidatSerializer(profil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)