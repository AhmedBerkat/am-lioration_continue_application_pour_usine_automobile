from django.contrib import admin
from .models import User, Demande, Alertechef,Alertequal,Alertemain, Tache

# Admin pour User
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'nom_prenom', 'role','poste','shift','created_at' ,'password')  # Affiche les champs dans la liste
    list_editable = ('role',)  # Permet d'éditer directement le rôle dans l'interface admin
    list_filter = ('role',)  # Ajoute un filtre par rôle
    search_fields = ('nom_prenom', 'role')  # Permet de rechercher par nom, prénom, ou rôle

admin.site.register(User, UserAdmin)

# Admin pour Demande
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    list_filter = ('statut',)  # Ajoute un filtre par statut
    search_fields = ('demande.id',)  # Permet de rechercher par type de matériel

admin.site.register(Demande, DemandeAdmin)

# Admin pour Alerte
class AlertemainAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    list_filter = ('statut',)  # Ajoute un filtre par statut
    search_fields = ('alertemain.id',)  # Permet de rechercher par type d'alerte

admin.site.register(Alertemain, AlertemainAdmin)

class AlertequalAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    list_filter = ('statut',)  # Ajoute un filtre par statut
    search_fields = ('alertequal.id',)  # Permet de rechercher par type d'alerte

admin.site.register(Alertequal, AlertequalAdmin)

class AlertechefAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    list_filter = ('statut',)  # Ajoute un filtre par statut
    search_fields = ('alertechef.id',)  # Permet de rechercher par type d'alerte

admin.site.register(Alertechef, AlertechefAdmin)
# Admin pour Tache
class TacheAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type_machine', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    list_filter = ('statut',)  # Ajoute un filtre par statut
    search_fields = ('type_machine',)  # Permet de rechercher par type de machine

admin.site.register(Tache, TacheAdmin)
