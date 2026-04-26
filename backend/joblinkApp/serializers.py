from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Le Serializer s'occupe de transformer les données JSON reçues du frontend en objets Python/Django
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # On ajoute un champ virtuel 'role' pour faciliter la communication avec le frontend (Angular)
    role = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_candidate', 'is_recruiter', 'role')

    def create(self, validated_data):
        # On extrait le rôle s'il est présent
        role = validated_data.pop('role', None)
        
        # Si le frontend a envoyé 'role', on met à jour les booléens correspondants
        if role == 'candidate':
            validated_data['is_candidate'] = True
        elif role == 'recruiter':
            validated_data['is_recruiter'] = True

        # On utilise create_user pour hacher le mot de passe automatiquement et créer l'utilisateur
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_candidate=validated_data.get('is_candidate', False),
            is_recruiter=validated_data.get('is_recruiter', False)
        )
        return user
    

# Serializer personnalisé pour le token JWT (utilisé lors de la connexion)
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # On appelle la validation standard pour obtenir les tokens access et refresh
        data = super().validate(attrs)
        
        # On ajoute des informations supplémentaires dans la réponse JSON de connexion
        # Cela évite au frontend de devoir faire une deuxième requête pour connaître le rôle
        data['is_candidate'] = self.user.is_candidate
        data['is_recruiter'] = self.user.is_recruiter
        data['username'] = self.user.username
        
        return data