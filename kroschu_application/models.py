from django.db import models
from django.contrib.auth.models import User  # Importer le modèle User intégré de Django pour la gestion des utilisateurs
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, user_id,nom_prenom, role,poste,shift, password=None ):
        if not user_id:
            raise ValueError("Les utilisateurs doivent avoir un identifiant")
        user = self.model(user_id=user_id, nom_prenom=nom_prenom, role=role,poste=poste,shift=shift)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, nom_prenom, role, poste,shift,password):
        user = self.create_user(user_id, nom_prenom, role,poste,shift ,password)
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
    SHIFT_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        
    ]

    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    nom_prenom= models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    poste = models.CharField(max_length=100)
    shift = models.CharField(max_length=50, choices=SHIFT_CHOICES)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout automatique

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['nom_prenom','role' ,'Shift' ,'poste']

    def __str__(self):
        return f"{self.user_id}"

# Modèle Demande
class Demande(models.Model):
    STATUT_CHOICES = [
        
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Référence à l'utilisateur via user_id
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')  # Nouveau champ statut
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout automatique
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Demande de {self.created_at} - {self.statut}"

# Modèle Alerte
class Alertemain(models.Model):
   
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id} - {self.created_at}  - {self.statut}"


class Alertequal(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id} - {self.created_at}  - {self.statut}"


class Alertechef(models.Model):
   
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Alerte de {self.user_id}- {self.created_at} - {self.statut}"


# Modèle Tache
class Tache(models.Model):
    TYPE_MACHINE_CHOICES = [
        ('soudage', 'Soudage'),
        ('sertissage', 'Sertissage'),
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
        return f"Alerte de {self.user_id} - {self.type_machine}  - {self.description}- {self.created_at}  - {self.statut}"
