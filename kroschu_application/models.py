from django.db import models
from django.contrib.auth.models import User  # Importer le modèle User intégré de Django pour la gestion des utilisateurs
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, user_id, nom, prenom, role, password=None ):
        if not user_id:
            raise ValueError("Les utilisateurs doivent avoir un identifiant")
        user = self.model(user_id=user_id, nom=nom, prenom=prenom, role=role)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, nom, prenom, role, password):
        user = self.create_user(user_id, nom, prenom, role, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = [
        ('operateur', 'Opérateur'),
        ('logistique', 'Logistique'),
        ('maintenance', 'Maintenance'),
        ('qualite', 'Qualité'),
        ('chef_equipe', 'Chef d\'équipe'),
    ]

    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout automatique

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['nom', 'prenom', 'role']

    def __str__(self):
        return f"{self.user_id}"

# Modèle Demande
class Demande(models.Model):
    TYPE_MATERIEL_CHOICES = [
        ('fil', 'Fil'),
        ('gaine', 'Gaine'),
        ('terminale', 'Terminale'),
        ('connecteur', 'Connecteur'),
    ]
    STATUT_CHOICES = [
        
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Référence à l'utilisateur via user_id
    type_materiel = models.CharField(max_length=100, choices=TYPE_MATERIEL_CHOICES)  # Choix du type de matériel
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')  # Nouveau champ statut
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout automatique
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Demande de {self.type_materiel} - {self.created_at} - {self.statut}"

# Modèle Alerte
class Alertemain(models.Model):
    TYPE_ALERTEM_CHOICES = [
        ('mecanique', 'Mécanique'),
        ('hydraulique', 'Hydraulique'),
        ('electrique', 'Électrique'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type_alertemain = models.CharField(max_length=100, choices=TYPE_ALERTEM_CHOICES)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id} - {self.type_alertemain} - {self.created_at}  - {self.statut}"


class Alertequal(models.Model):
    TYPE_ALERTE_CHOICES = [
        ('verification', 'Verification'),
        ('validation', 'Validation'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type_alertequal = models.CharField(max_length=100, choices=TYPE_ALERTE_CHOICES)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id} - {self.type_alertequal} - {self.created_at}  - {self.statut}"


class Alertechef(models.Model):
    TYPE_ALERTE_CHOICES = [
        ('assistance', 'Assistance'),
        ('autre', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    type_alertechef = models.CharField(max_length=100, choices=TYPE_ALERTE_CHOICES)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id} - {self.type_alertechef} - {self.created_at} - {self.statut}"


# Modèle Tache
class Tache(models.Model):
    TYPE_MACHINE_CHOICES = [
        ('soudage', 'Soudage'),
        ('sertissage', 'Sertissage'),
        ('coupage', 'Coupage'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Référence à l'utilisateur via user_id
    type_machine = models.CharField(max_length=100, choices=TYPE_MACHINE_CHOICES)  # Choix du type de machine
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')  # Nouveau champ statut
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout automatique
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id} - {self.type_machine} - {self.created_at} - {self.description}  - {self.statut}"
