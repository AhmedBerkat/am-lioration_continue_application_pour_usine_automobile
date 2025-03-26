from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

def determine_shift():
    """Détermine le shift actuel en fonction de l'heure."""
    current_hour = now().hour
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

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    def create_user(self, poste, role, password=None):
        """Crée et enregistre un utilisateur avec le poste, le rôle et le mot de passe donnés."""
        if not poste:
            raise ValueError("L'utilisateur doit avoir un poste.")
        user = self.model(poste=poste, role=role)
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
        ('logistique', 'Logistique'),
        ('maintenance', 'Maintenance'),
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

    @property
    def shift(self):
        return determine_shift()

    def __str__(self):
        return f"{self.poste}"

class Demande(BaseModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    
    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)

    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60  # Temps en minutes
        return None

    def __str__(self):
        return f"Demande de {self.poste} - {self.statut}"

class Alertemain(BaseModel):
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
        return f"Alerte Maintenance de {self.poste} - {self.statut}"

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
        return f"Alerte Qualité de {self.poste} - {self.statut}"

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
        return f"Alerte Chef de {self.poste} - {self.statut}"

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