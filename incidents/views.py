from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Incident
from .pagination import ArticlePageNumberPagination
from .serializers import *
from .permission import IsCitoyen, IsAdmin

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# --------------------------------------------------
#               INSCRIPTION UTILISATEUR
# --------------------------------------------------
@swagger_auto_schema(
    method='post',
    operation_id="Inscription",
    operation_description="Créer un nouveau compte utilisateur.",
    request_body=UtilisateurSerializer,
    responses={201: UtilisateurSerializer()}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Inscription d'un nouvel utilisateur.
    Accessible à tous.
    """
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------
#                   LOGIN UTILISATEUR
# --------------------------------------------------
@swagger_auto_schema(
    method='post',
    operation_id="Connexion",
    operation_description="Retourne un token JWT pour un utilisateur valide.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={200: openapi.Response("Token JWT", schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            'access': openapi.Schema(type=openapi.TYPE_STRING),
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'role': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ))}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Connexion utilisateur.
    Retourne access et refresh tokens si les identifiants sont valides.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'role': user.role,
        })
    return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

# --------------------------------------------------
#            AJOUTER UN INCIDENT PAR CITOYEN
# --------------------------------------------------
@swagger_auto_schema(
    method='post',
    operation_id="Déclarer un incident",
    operation_description="Permet à un citoyen de signaler un incident.",
    request_body=IncidentSerializer,
    responses={201: IncidentSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCitoyen])
def ajouter_incident(request):
    """
    Ajout d'un incident par un utilisateur citoyen.
    """
    serializer = IncidentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(utilisateur=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------
#     AFFICHER LES INCIDENTS DE L'UTILISATEUR
# --------------------------------------------------
@swagger_auto_schema(
    method='get',
    operation_id="Incidents de l'utilisateur",
    operation_description="Retourne les incidents déclarés par l'utilisateur connecté.",
    responses={200: IncidentSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCitoyen])
def mes_incidents(request):
    """
    Liste paginée des incidents de l'utilisateur connecté.
    """
    incidents = Incident.objects.filter(utilisateur=request.user).order_by('-date_creation')
    paginator = ArticlePageNumberPagination()
    result_page = paginator.paginate_queryset(incidents, request)
    serializer = IncidentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

# --------------------------------------------------
#         MODIFIER L'ÉTAT D'UN INCIDENT (ADMIN)
# --------------------------------------------------
@swagger_auto_schema(
    method='patch',
    operation_id="Modifier l'état d'un incident",
    operation_description="Permet à un admin de mettre à jour l'état d'un incident.",
    manual_parameters=[
        openapi.Parameter(
            'incident_id', openapi.IN_PATH,
            description="ID de l'incident",
            type=openapi.TYPE_INTEGER
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'etat': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['etat']
    ),
    responses={200: openapi.Response(description="État mis à jour")}
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def modifier_etat_incident(request, incident_id):
    """
    Modifier l'état d'un incident (admin uniquement).
    """
    try:
        incident = Incident.objects.get(id=incident_id)
    except Incident.DoesNotExist:
        return Response({"error": "Incident non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    new_etat = request.data.get("etat")
    if new_etat not in ["En ettant", "traité"]:
        return Response({"error": "État invalide"}, status=status.HTTP_400_BAD_REQUEST)

    incident.etat = new_etat
    incident.save()
    return Response({"message": "État mis à jour avec succès"})

# --------------------------------------------------
#        AFFICHER TOUS LES INCIDENTS (ADMIN)
# --------------------------------------------------
@swagger_auto_schema(
    method='get',
    operation_id="Liste de tous les incidents",
    operation_description="Retourne tous les incidents enregistrés (réservé aux administrateurs).",
    responses={200: IncidentSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def tous_les_incidents(request):
    """
    Liste paginée de tous les incidents (admin uniquement).
    """
    incidents = Incident.objects.all().order_by('-date_creation')
    paginator = ArticlePageNumberPagination()
    result_page = paginator.paginate_queryset(incidents, request)
    serializer = IncidentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
