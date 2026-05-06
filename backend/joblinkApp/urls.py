from django.urls import path
from .views import RegisterView, api_root, ProfilCandidatView

urlpatterns = [
    path('', api_root, name='api-root'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('profil/', ProfilCandidatView.as_view(), name='profil-candidat'),
]