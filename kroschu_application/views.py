from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User, Demande,Alertemain,Alertequal, Alertechef,Tache
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import User
from . import models
from .models import *
from django.utils.timezone import now
from django.utils import timezone
from django.shortcuts import  redirect
from datetime import timedelta
from django.contrib.auth import logout
def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        poste = request.POST['poste']
      
        role = request.POST['role']
       
        
        password = request.POST['password']
        
        new_user = User(poste=poste, role=role,password=make_password(password))
        new_user.save()
        return redirect('kroschu_application:login_view')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        poste = request.POST['poste']
        password = request.POST['password']
        
        user = authenticate(request, username=poste, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'operateur':
                return redirect('kroschu_application:operateur_dashboard')
            elif user.role == 'logistique':
                return redirect('kroschu_application:logistique_dashboard')
            elif user.role == 'maintenance':
                return redirect('kroschu_application:maintenance_dashboard')
            elif user.role == 'qualite':
                return redirect('kroschu_application:qualite_dashboard')
            else:
                return redirect('kroschu_application:chef_equipe_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Identifiant ou mot de passe incorrect'})

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('kroschu_application:home_view') 

@login_required
def operateur_dashboard(request):
    operateur = request.user
    taches = Tache.objects.filter(poste=operateur).filter(statut='en_attente')
    demandes = Demande.objects.filter(poste=operateur).filter(statut='en_attente')
    
    alertemains =Alertemain.objects.filter(poste=operateur).filter(statut='en_attente')
    alertequals=Alertequal.objects.filter(poste=operateur).filter(statut='en_attente')
    alertechefs =Alertechef.objects.filter(poste=operateur).filter(statut='en_attente')

    # Passer ces données au template
    context = {
        'taches': taches,
        'demandes': demandes,
        'alertemains': alertemains,
        'alertequals': alertequals,
        'alertechefs': alertechefs,
    }
    return render(request, 'operateur_dashboard.html', context)

@login_required
def demande_materiel(request):
    if request.method == 'POST':
        Demande.objects.create(poste=request.user,statut='en_attente')
        return redirect('kroschu_application:operateur_dashboard')

@login_required
def alerte_maintenance(request):
    if request.method == 'POST': 
        # Création de l'alerte dans la base de données
        Alertemain.objects.create(
            poste=request.user, 
            statut='en_attente',
            
        )
        return redirect('kroschu_application:operateur_dashboard')

@login_required
def alerte_chef(request):
    if request.method == 'POST':
        # Création de l'alerte dans la base de données
        Alertechef.objects.create(
            poste=request.user,
            statut='en_attente',
                        
        )
        return redirect('kroschu_application:operateur_dashboard')

@login_required
def alerte_qualite(request):
    if request.method == 'POST':
        # Création de l'alerte dans la base de données
        Alertequal.objects.create(
            poste=request.user, 
            statut='en_attente', 
            
        )
        return redirect('kroschu_application:operateur_dashboard')



@login_required
def logistique_dashboard(request):
    demandes = Demande.objects.all().order_by(
        models.Case(
            models.When(statut="en_attente", then=0),
            models.When(statut="traite", then=1),
            default=2,
            output_field=models.IntegerField()
        ),
        "-created_at"
    )

    return render(request, 'logistique_dashboard.html', {'demandes': demandes})



@login_required
def maintenance_dashboard(request):
    alertemains = Alertemain.objects.all().order_by(
        models.Case(
            models.When(statut="en_attente", then=0),
            models.When(statut="traite", then=1),
            default=2,
            output_field=models.IntegerField()
        ),
        "-created_at"
    )
    return render(request, 'maintenance_dashboard.html', {'alertemains': alertemains})

@login_required
def qualite_dashboard(request):
    alertequals = Alertequal.objects.all().order_by(
        models.Case(
            models.When(statut="en_attente", then=0),
            models.When(statut="traite", then=1),
            default=2,
            output_field=models.IntegerField()
        ),
        "-created_at"
    )
    return render(request, 'qualite_dashboard.html', {'alertequals': alertequals})


@login_required
def chef_equipe_dashboard(request):
    operateurs = User.objects.all().order_by('-created_at')
    taches = Tache.objects.all().order_by(
        models.Case(
            models.When(statut="en_attente", then=0),
            models.When(statut="traite", then=1),
            default=2,
            output_field=models.IntegerField()
        ),
        "-created_at"
    )
    alertechefs = Alertechef.objects.all().order_by(
        models.Case(
            models.When(statut="en_attente", then=0),
            models.When(statut="traite", then=1),
            default=2,
            output_field=models.IntegerField()
        ),
        "-created_at"
    )
    return render(request, 'chef_equipe_dashboard.html', {
        'taches': taches,
        'operateurs': operateurs,
        'alertechefs': alertechefs
    })


@login_required
def valider_demande(request, demande_id):
    try:
        # Récupérer la demande par son ID
        demande = Demande.objects.get(id=demande_id)

        # Vérifier que la demande appartient à l'utilisateur
        if demande.poste == request.user and demande.statut == 'en_attente':
            # Mettre à jour le statut de la demande
            demande.statut = 'traité'
            demande.validated_at = now()
            demande.save()
        else:
            # Si l'utilisateur n'est pas propriétaire de la demande
            return redirect('kroschu_application:operateur_dashboard')
        
        return redirect('kroschu_application:operateur_dashboard')
    except Demande.DoesNotExist:
        # Si la demande n'existe pas
        return redirect('kroschu_application:operateur_dashboard')
    


@login_required
def affecter_tache(request):
    # Récupérer tous les opérateurs
    operateurs = User.objects.filter(role='operateur')

    if request.method == "POST":
        # Récupérer les données du formulaire
        poste = request.POST.get('poste')
        type_machine = request.POST.get('type_machine')
        description=request.POST.get('description', '')
        if poste and type_machine and description:
            operateur = User.objects.get(poste=poste)
            tache = Tache.objects.create(
                poste=operateur,
                type_machine=type_machine,
                description=description,
                statut="en_attente",
            )
            tache.save()

        return redirect('kroschu_application:chef_equipe_dashboard')  # Rediriger vers le tableau de bord du chef d'équipe

    return render(request, 'affecter_tache.html', {'operateurs': operateurs})




@login_required
def signaler_tache_terminee(request, tache_id):
    try:
        tache = Tache.objects.get(id=tache_id)
        if tache.poste == request.user and tache.statut == 'en_attente':  # Vérifie si la tâche appartient à l'utilisateur connecté
            tache.statut = 'traité'
            tache.validated_at = now()
            tache.save()
        else:
            # Si l'utilisateur n'est pas l'opérateur de la tâche, il n'a pas l'autorisation de la modifier
            return redirect('kroschu_application:operateur_dashboard')  # Redirection vers le tableau de bord opérateur
    except Tache.DoesNotExist:
        # Si la tâche n'existe pas, redirige
        return redirect('kroschu_application:operateur_dashboard')
    
    return redirect('kroschu_application:operateur_dashboard')  # Redirection après avoir modifié la tâche

@login_required
def valider_alerte_maintenance(request, alertemain_id):
    try:
        alertemain = Alertemain.objects.get(id=alertemain_id)
        if alertemain.poste == request.user and alertemain.statut == 'en_attente':  # Vérifie si la tâche appartient à l'utilisateur connecté
            alertemain.statut = 'traité'
            alertemain.validated_at = now()
            alertemain.save()
        else:
            # Si l'utilisateur n'est pas l'opérateur de la tâche, il n'a pas l'autorisation de la modifier
            return redirect('kroschu_application:operateur_dashboard')  # Redirection vers le tableau de bord opérateur
    except Alertemain.DoesNotExist:
        # Si la tâche n'existe pas, redirige
        return redirect('kroschu_application:operateur_dashboard')
    
    return redirect('kroschu_application:operateur_dashboard')  # Redirection après avoir modifié la tâche

@login_required
def valider_alerte_qualite(request, alertequal_id):
    try:
        alertequal = Alertequal.objects.get(id=alertequal_id)
        if alertequal.poste == request.user and alertequal.statut == 'en_attente':  # Vérifie si la tâche appartient à l'utilisateur connecté
            alertequal.statut = 'traité'
            alertequal.validated_at = now()
            alertequal.save()
        else:
            # Si l'utilisateur n'est pas l'opérateur de la tâche, il n'a pas l'autorisation de la modifier
            return redirect('kroschu_application:operateur_dashboard')  # Redirection vers le tableau de bord opérateur
    except Alertequal.DoesNotExist:
        # Si la tâche n'existe pas, redirige
        return redirect('kroschu_application:operateur_dashboard')
    
    return redirect('kroschu_application:operateur_dashboard')  # Redirection après avoir modifié la tâche

@login_required
def valider_alerte_chef(request, alertechef_id):
    try:
        alertechef = Alertechef.objects.get(id=alertechef_id)
        if alertechef.poste == request.user and alertechef.statut == 'en_attente':  # Vérifie si la tâche appartient à l'utilisateur connecté
            alertechef.statut = 'traité'
            alertechef.validated_at = now()
            alertechef.save()
        else:
            # Si l'utilisateur n'est pas l'opérateur de la tâche, il n'a pas l'autorisation de la modifier
            return redirect('kroschu_application:operateur_dashboard')  # Redirection vers le tableau de bord opérateur
    except Alertechef.DoesNotExist:
        # Si la tâche n'existe pas, redirige
        return redirect('kroschu_application:operateur_dashboard')
    
    return redirect('kroschu_application:operateur_dashboard')  # Redirection après avoir modifié la tâche







