from django.contrib import admin
from .models import User, Demande, Alertechef,Alertequal,Alertemain, Tache ,Wire

# Admin pour User
class UserAdmin(admin.ModelAdmin):
    list_display = ('poste', 'role','zone','shift','created_at' ,'password')  # Affiche les champs dans la liste
    list_editable = ('role',)  # Permet d'éditer directement le rôle dans l'interface admin
    list_filter = ('role',)  # Ajoute un filtre par rôle
    search_fields = ('zone',)  # Permet de rechercher par nom, prénom, ou rôle

admin.site.register(User, UserAdmin) 

class WireAdmin(admin.ModelAdmin):
    list_display = ('ident_code', 'section', 'length', 'color', 'position', 'created_at')
    search_fields = ('ident_code',)
    list_filter = ('ident_code',)

class TacheAdmin(admin.ModelAdmin):
    list_display = ('poste', 'ident_code', 'ident_type', 'type_machine', 'statut', 'created_at')
    list_filter = ('ident_type', 'statut', 'type_machine')
    search_fields = ('ident_code', 'poste__poste')
    list_editable = ('statut',)



admin.site.register(Wire, WireAdmin)
admin.site.register(Tache, TacheAdmin)

# Admin pour Demande

# Filtre personnalisé pour les demandes traitées et non traitées
class StatutDemandeFilter(admin.SimpleListFilter): 
    title = 'Statut de la demande'
    parameter_name = 'statut_demande'

    def lookups(self, request, model_admin):
        return (
            ('traite', 'Demandes traitées'),
            ('en_attente', 'Demandes non traitées'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'traite':
            return queryset.filter(statut='traite')  # Remplacer 'traite' par le statut correspondant
        if self.value() == 'en_attente':
            return queryset.filter(statut='en_attente')  # Remplacer 'non_traite' par le statut correspondant
        return queryset

# Admin pour Demande
class DemandeAdmin(admin.ModelAdmin):
    list_display = ('poste','statut', 'created_at','validated_at')  # Affiche les champs dans la liste
    list_filter = (StatutDemandeFilter, 'statut')  # Ajoute un filtre personnalisé pour les demandes traitées ou non traitées
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    search_fields = ('poste',)  # Permet de rechercher par poste

    # Personnalisation pour rendre la table plus lisible
    ordering = ('-created_at',)  # Tri les demandes par date de création, de la plus récente à la plus ancienne
    date_hierarchy = 'created_at'  # Permet d'ajouter une hiérarchie de dates pour un meilleur filtrage

admin.site.register(Demande, DemandeAdmin)


class StatutAlerteFilter(admin.SimpleListFilter):
    title = 'Statut de l\'alerte'
    parameter_name = 'statut_alerte'

    def lookups(self, request, model_admin):
        return (
            ('traite', 'Alertes traitées'),
            ('non_traite', 'Alertes non traitées'),
        )

    def queryset(self, request, queryset): 
        if self.value() == 'traite': 
            return queryset.filter(statut='traite')  # Remplacer 'traite' par le statut correspondant
        if self.value() == 'non_traite':
            return queryset.filter(statut='non_traite')  # Remplacer 'non_traite' par le statut correspondant
        return queryset

# Admin pour Alertemain
class AlertemainAdmin(admin.ModelAdmin):
    list_display = ('poste', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_filter = (StatutAlerteFilter, 'statut')  # Ajoute le filtre personnalisé pour les alertes traitées ou non traitées
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    search_fields = ('poste',)  # Permet de rechercher par poste

    # Personnalisation pour rendre la table plus lisible
    ordering = ('-created_at',)  # Tri les alertes par date de création, de la plus récente à la plus ancienne
    date_hierarchy = 'created_at'  # Permet d'ajouter une hiérarchie de dates pour un meilleur filtrage

admin.site.register(Alertemain, AlertemainAdmin)

# Admin pour Alertequal
class AlertequalAdmin(admin.ModelAdmin):
    list_display = ('poste', 'statut', 'created_at') # Affiche les champs dans la liste
    list_filter = (StatutAlerteFilter, 'statut') # Ajoute le filtre personnalisé pour les alertes traitées ou non traitées
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    search_fields = ('poste',)  # Permet de rechercher par poste

    # Personnalisation pour rendre la table plus lisible
    ordering = ('-created_at',)  # Tri les alertes par date de création, de la plus récente à la plus ancienne
    date_hierarchy = 'created_at'  # Permet d'ajouter une hiérarchie de dates pour un meilleur filtrage

admin.site.register(Alertequal, AlertequalAdmin)

# Admin pour Alertechef
class AlertechefAdmin(admin.ModelAdmin):
    list_display = ('poste', 'statut', 'created_at')  # Affiche les champs dans la liste
    list_filter = (StatutAlerteFilter, 'statut')  # Ajoute le filtre personnalisé pour les alertes traitées ou non traitées
    list_editable = ('statut',)  # Permet d'éditer directement le statut dans l'interface admin
    search_fields = ('poste',)  # Permet de rechercher par poste

    # Personnalisation pour rendre la table plus lisible
    ordering = ('-created_at',)  # Tri les alertes par date de création, de la plus récente à la plus ancienne
    date_hierarchy = 'created_at'  # Permet d'ajouter une hiérarchie de dates pour un meilleur filtrage

admin.site.register(Alertechef, AlertechefAdmin) 