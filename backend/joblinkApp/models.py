from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class ProfilCandidat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nom = models.CharField(max_length=100)
    competences = models.TextField(blank=True)
    diplomes = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.email}"

class Candidature(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('vue', 'Vue'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]
    candidat = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidatures')
    offre_titre = models.CharField(max_length=200)
    entreprise = models.CharField(max_length=200)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    date_candidature = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidat.email} - {self.offre_titre} ({self.statut})"