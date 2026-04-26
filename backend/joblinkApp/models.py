from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    # On définit des booléens pour identifier les rôles
    email = models.EmailField(unique=True)
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)

    # On peut aussi ajouter des champs supplémentaires communs
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] # Le username reste requis par Django mais n'est plus l'identifiant de login

    def __str__(self):
        return self.email