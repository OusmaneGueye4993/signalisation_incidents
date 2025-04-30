from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser, Group, Permission
from rest_framework.decorators import api_view, permission_classes





class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Incident(models.Model):
    photo = models.ImageField(upload_to='incidents_photos/', null=True, blank=True)
    logitude = models.FloatField()
    latitude = models.FloatField()
    description_texte = models.TextField()
    description_vocale = models.FileField(
        upload_to='incidents_vocal/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav'])]
    )
    ROLE_CHOICES = (
        ('En ettant', 'En ettant'),
        ('traité', 'traité'),
    )
    etat = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='incidents')
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='incidents', null=True, blank=True)  # Nouveau champ

    def __str__(self):
        return f"Incident {self.id} - {self.etat}"

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('citoyen', 'Citoyen'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='utilisateur_groups',
        blank=True,
        help_text="Les groupes auxquels cet utilisateur appartient."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='utilisateur_permissions',
        blank=True,
        help_text="Permissions spécifiques de l'utilisateur."
    )

    def __str__(self):
        return self.username

  
