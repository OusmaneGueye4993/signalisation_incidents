from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Incident
from .pagination import ArticlePageNumberPagination
from .serializers import *
from .permission import IsCitoyen, IsAdmin
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
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
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCitoyen])
def ajouter_incident(request):
    serializer = IncidentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(utilisateur=request.user)  # Lier au citoyen connecté
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCitoyen])
def mes_incidents(request):
    incidents = Incident.objects.filter(utilisateur=request.user).order_by('-date_creation')
    paginator = ArticlePageNumberPagination()
    result_page = paginator.paginate_queryset(incidents, request)
    serializer = IncidentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsAdmin])
def modifier_etat_incident(request, incident_id):
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


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def tous_les_incidents(request):
    incidents = Incident.objects.all().order_by('-date_creation')
    paginator = ArticlePageNumberPagination()
    result_page = paginator.paginate_queryset(incidents, request)
    serializer = IncidentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)