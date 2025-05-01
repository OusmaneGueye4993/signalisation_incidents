
from django.conf import settings
from django.conf.urls.static import static
from .views import register
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib import admin
from django.urls import path
from .views import login,ajouter_incident, mes_incidents, modifier_etat_incident,tous_les_incidents,liste_utilisateurs,modifier_role_utilisateur,deleteUser

urlpatterns = [
   
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'), 
    path('api/incidents/ajouter/', ajouter_incident, name='ajouter_incident'),
    path('api/incidents/mes/', mes_incidents, name='mes_incidents'),
    path('api/incidents/modifier-etat/<int:incident_id>/', modifier_etat_incident, name='modifier_etat'),
    path('api/tous_les_incidents', tous_les_incidents, name='tous_les_incidents'),
    path('api/utilisateurs/', liste_utilisateurs, name='liste_utilisateurs'),
    path('api/utilisateurs/<int:user_id>/deleteUser/', deleteUser, name='deleteUser'),
    path('api/utilisateurs/<int:user_id>/modifier-role/', modifier_role_utilisateur, name='modifier_role_utilisateur'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
