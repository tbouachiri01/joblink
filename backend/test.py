from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, ProfilCandidat

class ProfilCandidatTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='pass1234'
        )
        self.client.force_authenticate(user=self.user)

    def test_creer_profil(self):
        data = {'nom': 'Manil', 'competences': 'Python', 'diplomes': 'Licence', 'experience': '2 ans'}
        response = self.client.post('/api/profil/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_profil(self):
        ProfilCandidat.objects.create(user=self.user, nom='Manil')
        response = self.client.get('/api/profil/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profil(self):
        ProfilCandidat.objects.create(user=self.user, nom='Ancien')
        response = self.client.put('/api/profil/', {'nom': 'Nouveau'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nom'], 'Nouveau')

    def test_non_authentifie(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/profil/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)