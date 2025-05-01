from rest_framework import serializers
from .models import Utilisateur, Incident


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ('id', 'username', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.get('role', 'citoyen')  # Par défaut "citoyen"
        user = Utilisateur.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password'],
        
    )
        user.is_active = True  
        user.save()
        return user


    

class IncidentSerializer(serializers.ModelSerializer):
    utilisateur = serializers.StringRelatedField(read_only=True)  # Affiche le nom d'utilisateur

    class Meta:
        model = Incident
        fields = ('id', 'photo', 'logitude', 'latitude', 'description_texte', 'description_vocale', 'etat', 'date_creation', 'category', 'utilisateur')
        read_only_fields = ('date_creation',)






