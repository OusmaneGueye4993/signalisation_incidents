from django.contrib import admin
from .models import Incident, Category,Utilisateur


class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'logitude', 'latitude', 'description_texte', 'description_vocale', 'etat', 'date_creation')
    search_fields = ('description_texte',)
    list_filter = ('etat',)
    ordering = ('-date_creation',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    ordering = ('username',)    


admin.site.register(Incident, IncidentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)