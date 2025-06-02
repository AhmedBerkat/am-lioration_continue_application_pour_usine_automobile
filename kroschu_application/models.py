from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now ,localtime
from django.utils import timezone
from django.core.management.base import BaseCommand
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

class Wire(models.Model):
    ident_code = models.CharField(max_length=50, help_text="V_ident or P_ident code (e.g., V56876485353)")
    section = models.FloatField(help_text="Wire section (e.g., 0.2, 0.5, 1.0)")
    length = models.FloatField(help_text="Wire length in meters")
    color = models.CharField(max_length=50, help_text="Wire color")
    position = models.CharField(max_length=100, help_text="Position (e.g., Two right, one left)")
    L_ident = models.CharField(max_length=50)
    version = models.CharField(max_length=10, help_text="Version of the wire (e.g., v1, v2)", default="v1")  # Nouveau champ
    created_at = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return f"Wire for {self.ident_code}: {self.section}mm², {self.length}m, {self.color}, {self.position}"

class UserManager(BaseUserManager):
    def create_user(self, poste, role, password=None ,**extra_fields):
        """Crée et enregistre un utilisateur avec le poste, le rôle et le mot de passe donnés."""
        if not poste:
            raise ValueError("L'utilisateur doit avoir un poste.")
        user = self.model(poste=poste, role=role , **extra_fields)
        user.set_password(password)  # Hash du mot de passe ici <---
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
        ('qualite_vk', 'Qualité_VK'),
        ('qualite_cutting', 'Qualité_Cutting'),
        ('qualite_ksk', 'Qualité_Ksk'),
        ('chef_vk', 'Chef_VK'),
        ('chef_cutting', 'Chef_Cutting'),
        ('chef_ksk', 'Chef_Ksk'),
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
    wires = models.ManyToManyField(Wire, blank=True, help_text="Wires requested for this demande")
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
    Qualite_CHOICES = [
        ('qualite_vk', 'Qualité VK'),
        ('qualite_cutting', 'Qualité Cutting '),
        ('qualite_ksk', 'Qualité KSK '),

    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    qualite_type = models.CharField(max_length=50, choices=Qualite_CHOICES, null=True, blank=True)
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
    CHEF_TYPE_CHOICES = [
        ('chef_vk', 'Chef VK'),
        ('chef_ksk', 'Chef KSK'),
        ('chef_cutting', 'Chef Cutting'),
    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    chef_type = models.CharField(max_length=50, choices=CHEF_TYPE_CHOICES, null=True, blank=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)


    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60
        return None


    def __str__(self):
        return f"Alerte Chef de {self.poste} - {self.statut}-{self.shift}- {self.chef_type}"

class Machine(models.Model):
    name = models.CharField(max_length=50, unique=True)
    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='machines', limit_choices_to={'role': 'operateur'})
    is_occupied = models.BooleanField(default=False)
    current_task = models.ForeignKey('Tache', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_machine')
    queued_tasks = models.ManyToManyField('Tache', related_name='queued_on_machine', blank=True)
    task_count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.name} (Poste: {self.poste.poste if self.poste else 'N/A'})"


class Tache(BaseModel):
    TYPE_MACHINE_CHOICES = [
        ('soudage', 'Soudage'),
        ('sertissage', 'Sertissage'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('traité', 'Traité'),
    ]
    IDENT_TYPE_CHOICES = [
        ('V_ident', 'V_ident'),
        ('PM', 'PM'),
    ]

    poste = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    machine = models.ForeignKey(Machine, on_delete=models.SET_NULL, null=True, blank=True,related_name='assigned_tasks')
    type_machine = models.CharField(max_length=100, choices=TYPE_MACHINE_CHOICES)
    ident_type = models.CharField(max_length=20, choices=IDENT_TYPE_CHOICES, null=True, blank=True)
    version = models.CharField(max_length=10, help_text="Version of the task (e.g., v1, v2)", default="v1")  # Nouveau champ
    ident_code = models.CharField(max_length=50, null=True, blank=True, help_text="V_ident or PM code")
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='en_attente')
    validated_at = models.DateTimeField(null=True, blank=True)

    def temps_de_traitement(self):
        if self.validated_at:
            return (self.validated_at - self.created_at).total_seconds() / 60
        return None

    def __str__(self):
        return f"Tâche {self.type_machine} pour {self.poste} - {self.statut}"
    
