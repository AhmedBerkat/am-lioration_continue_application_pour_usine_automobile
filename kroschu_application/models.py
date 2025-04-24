from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now ,localtime
from django.utils import timezone
def determine_shift(datetime=None):
    """Détermine le shift en fonction de l'heure."""
    if datetime is None:
        datetime = now()

    current_hour = localtime(datetime).hour

    if 22 <= current_hour or current_hour < 6:
        return 'A'
    elif 6 <= current_hour < 14:
        return 'B'
    else:
        return 'C'
class BaseModel(models.Model):
    """Classe de base pour ajouter des champs communs à tous les modèles."""
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shift = models.CharField(max_length=1)


    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not isinstance(self, User):  # Ne pas calculer pour User
            if not self.pk:  # Nouvel objet
                self.shift = determine_shift()
            else:  # Objet existant
                original = type(self).objects.get(pk=self.pk)
                if original.created_at != self.created_at:
                    self.shift = determine_shift(self.created_at)
        super().save(*args, **kwargs)

class UserManager(BaseUserManager):
    def create_user(self, poste, role, password=None ,**extra_fields):
        """Crée et enregistre un utilisateur avec le poste, le rôle et le mot de passe donnés."""
        if not poste:
            raise ValueError("L'utilisateur doit avoir un poste.")
        user = self.model(poste=poste, role=role , **extra_fields)
        user.set_password(password)  # Hash du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, poste, password, **extra_fields):
        """Crée et enregistre un superutilisateur avec le poste et le mot de passe donnés."""
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('role') != 'admin':
            raise ValueError('Le superutilisateur doit avoir le rôle "admin".')
        return self.create_user(poste, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES = [
        ('operateur', 'Opérateur'),
        ('logistique_incomming', 'Logistique_Incomming'),
        ('logistique_pagoda', 'Logistique_Pagoda'),
        ('logistique_kit', 'Logistique_Kit'),
        ('maintenance_machine', 'Maintenance_Machine'),
        ('maintenance_board', 'Maintenance_Board'),
        ('qualite', 'Qualité'),
        ('chef_equipe', 'Chef d\'équipe'),
        ('admin', 'Administrateur'),
    ]

    poste = models.CharField(max_length=50, unique=True, primary_key=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    zone = models.TextField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'poste'
    REQUIRED_FIELDS = ['role']



    def __str__(self):
        return f"{self.poste}"

class Demande(BaseModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    LOGISTIQUE_CHOICES = [
        ('logistique_incomming', 'Logistique Incomming'),
        ('logistique_pagoda', 'Logistique Pagoda'),
        ('logistique_kit', 'Logistique Kit'),
    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    logistique_type = models.CharField(max_length=50, choices=LOGISTIQUE_CHOICES, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)

    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Demande de {self.poste} - {self.statut} -{self.shift}"

class Alertemain(BaseModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    MAINTENANCE_CHOICES = [
        ('maintenance_board', 'Maintenance Board'),
        ('maintenance_machine', 'Maintenance Machine'),

    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    maintenance_type = models.CharField(max_length=50, choices=MAINTENANCE_CHOICES, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)

    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60
        return None


    def __str__(self):
        return f"Alerte Maintenance de {self.poste} - {self.statut} -{self.shift}"

class Alertequal(BaseModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)



    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60
        return None


    def __str__(self):
        return f"Alerte Qualité de {self.poste} - {self.statut}-{self.shift}"

class Alertechef(BaseModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)


    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60
        return None


    def __str__(self):
        return f"Alerte Chef de {self.poste} - {self.statut}-{self.shift}"

class Tache(BaseModel):
    TYPE_MACHINE_CHOICES = [
        ('soudage', 'Soudage'),
        ('sertissage', 'Sertissage'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    type_machine = models.CharField(max_length=100, choices=TYPE_MACHINE_CHOICES)
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)

    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60
        return None

    def __str__(self):
        return f"Tâche {self.type_machine} pour {self.poste} - {self.statut}"