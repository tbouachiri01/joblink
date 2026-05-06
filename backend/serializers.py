from rest_framework import serializers
from .models import User, ProfilCandidat
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_candidate', 'is_recruiter', 'role')

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        if role == 'candidate':
            validated_data['is_candidate'] = True
        elif role == 'recruiter':
            validated_data['is_recruiter'] = True
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_candidate=validated_data.get('is_candidate', False),
            is_recruiter=validated_data.get('is_recruiter', False)
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_candidate'] = self.user.is_candidate
        data['is_recruiter'] = self.user.is_recruiter
        data['username'] = self.user.username
        return data

class ProfilCandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilCandidat
        fields = ['id', 'nom', 'competences', 'diplomes', 'experience', 'cv']

    def validate_cv(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("CV max 5 Mo.")
            ext = value.name.split('.')[-1].lower()
            if ext not in ['pdf', 'doc', 'docx']:
                raise serializers.ValidationError("PDF ou Word uniquement.")
        return value