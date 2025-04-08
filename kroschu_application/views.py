from django.shortcuts import render, redirect ,get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Demande,Alertemain,Alertequal, Alertechef,Tache
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
import csv
from django.http import HttpResponse

from . import models
from .models import *
from django.utils.timezone import now
from django.utils import timezone
from django.shortcuts import  redirect
from datetime import timedelta
from django.contrib.auth import logout
def home(request):
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
            if user.is_superuser:  # Si l'utilisateur est un superutilisateur
                return redirect('kroschu_application:admin_postes')
            elif user.role == 'operateur':
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
    return redirect('kroschu_application:home') 


@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('kroschu_application:home')  # Empêcher l'accès aux non-admins
    
    demandes = Demande.objects.all()
    alertemains = Alertemain.objects.all()
    alertequals = Alertequal.objects.all()
    alertechefs = Alertechef.objects.all()
    taches = Tache.objects.all()

    context = {
        'demandes': demandes,
        'alertemains': alertemains,
        'alertequals': alertequals,
        'alertechefs': alertechefs,
        'taches': taches
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def operateur_dashboard(request):
    poste = request.user
    taches = Tache.objects.filter(poste=poste).filter(statut='en_attente')
    demandes = Demande.objects.filter(poste=poste).filter(statut='en_attente')
    
    alertemains =Alertemain.objects.filter(poste=poste).filter(statut='en_attente')
    alertequals=Alertequal.objects.filter(poste=poste).filter(statut='en_attente')
    alertechefs =Alertechef.objects.filter(poste=poste).filter(statut='en_attente')

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

##################################################################################################################

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_poste(request):
    if request.method == 'POST':
        poste = request.POST['poste']
      
        role = request.POST['role']
        zone = request.POST['zone']
        
        password = request.POST['password']
        
        new_user = User(poste=poste, role=role, zone=zone,password=make_password(password))
        new_user.save()
        return redirect('kroschu_application:admin_postes')
    
    return render(request, 'admin_postes.html')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def soft_deleteposte(request, model_name,poste):
    models_map = {
        'user': User,
    }
    model = models_map.get(model_name)
    if model:
        obj = get_object_or_404(model, poste=poste)  # Recherche par ID au lieu de 'poste'
        obj.is_deleted = True
        obj.save()

    return redirect('kroschu_application:admin_postes') 
@login_required
@user_passes_test(lambda u: u.is_superuser)
def soft_deletedem(request, model_name, id):
    models_map = {
        'demande': ('Demande', 'kroschu_application:admin_demandes'),
        'alertemain': ('Alertemain', 'kroschu_application:admin_alertes_maintenance'),
        'alertequal': ('Alertequal', 'kroschu_application:admin_alertes_qualite'),
        'alertechef': ('Alertechef', 'kroschu_application:admin_alertes_chef'),
    }

    model_info = models_map.get(model_name)
    
    if model_info:
        model_class = globals()[model_info[0]]  # Récupère la classe du modèle via son nom
        obj = get_object_or_404(model_class, id=id)
        obj.is_deleted = True
        obj.save()
        return redirect(model_info[1])  # Redirection dynamique selon le modèle

    return redirect('kroschu_application:admin_demandes') 



        

#######################################################################################################
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_postes(request):
    # Récupérer tous les postes
    postes = User.objects.filter(is_deleted=False)

    if request.method == 'POST':
        # Ajouter un nouveau poste
        poste = request.POST.get('poste')
        zone = request.POST.get('zone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        User.objects.create_user(poste=poste, role=role,zone=zone, password=password)
        return redirect('kroschu_application:admin_postes')

    context = {
        'postes': postes,
    }
    return render(request, 'admin_postes.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_demandes(request):
    # Filtres pour les demandes
    statut_filter = request.GET.get('statut')
    poste_filter = request.GET.get('poste')
    date_filter = request.GET.get('date')

    demandes = Demande.objects.filter(is_deleted=False)
    if statut_filter:
        demandes = demandes.filter(statut=statut_filter)
    if poste_filter:
        demandes = demandes.filter(poste__poste__icontains=poste_filter)
    if date_filter:
        demandes = demandes.filter(created_at__date=date_filter)

    context = {
        'demandes': demandes,
    }
    return render(request, 'admin_demandes.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_alertes_maintenance(request):
    # Filtres pour les alertes maintenance
    statut_filter = request.GET.get('statut')
    poste_filter = request.GET.get('poste')
    date_filter = request.GET.get('date')

    alertemains = Alertemain.objects.filter(is_deleted=False)
    if statut_filter:
        alertemains = alertemains.filter(statut=statut_filter)
    if poste_filter:
        alertemains = alertemains.filter(poste__poste__icontains=poste_filter)
    if date_filter:
        alertemains = alertemains.filter(created_at__date=date_filter)

    context = {
        'alertemains': alertemains,
    }
    return render(request, 'admin_alertes_maintenance.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_alertes_qualite(request):
    # Filtres pour les alertes qualité
    statut_filter = request.GET.get('statut')
    poste_filter = request.GET.get('poste')
    date_filter = request.GET.get('date')

    alertequals = Alertequal.objects.filter(is_deleted=False)
    if statut_filter:
        alertequals = alertequals.filter(statut=statut_filter)
    if poste_filter:
        alertequals = alertequals.filter(poste__poste__icontains=poste_filter)
    if date_filter:
        alertequals = alertequals.filter(created_at__date=date_filter)

    context = {
        'alertequals': alertequals,
    }
    return render(request, 'admin_alertes_qualite.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_alertes_chef(request):
    # Filtres pour les alertes chef d'équipe
    statut_filter = request.GET.get('statut')
    poste_filter = request.GET.get('poste')
    date_filter = request.GET.get('date')

    alertechefs = Alertechef.objects.filter(is_deleted=False)
    if statut_filter:
        alertechefs = alertechefs.filter(statut=statut_filter)
    if poste_filter:
        alertechefs = alertechefs.filter(poste__poste__icontains=poste_filter)
    if date_filter:
        alertechefs = alertechefs.filter(created_at__date=date_filter)

    context = {
        'alertechefs': alertechefs,
    }
    return render(request, 'admin_alertes_chef.html', context)




####################################################################################""


@login_required
def export_data(request):
    data_type = request.GET.get('type', '').lower()
    
    def safe_get_user_info(obj):
        """Helper function to safely get user info with all edge cases handled"""
        if not hasattr(obj, 'poste'):
            return ("Inconnu", "N/A")
            
        if obj.poste is None:
            return ("Utilisateur supprimé", "N/A")
            
        try:
            if obj.poste and not obj.poste.is_deleted:
                return (obj.poste.poste, obj.poste.shift)
            return ("Utilisateur supprimé", "N/A")
        except:
            return ("Erreur", "N/A")

    def calculate_time_elapsed(created, validated):
        """Calculate minutes between two datetime objects"""
        if not validated:
            return "En attente"
        try:
            delta = validated - created
            return f"{delta.total_seconds() / 60:.2f}"  # Convert to minutes with 2 decimals
        except Exception as e:
            print(f"Error calculating time: {e}")
            return "N/A"

    # Common CSV headers
    common_headers = ['ID', 'Poste', 'Shift', 'Date création', 'Statut', 'Temps écoulé (min)']
    
    if data_type == "demandes":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="demandes_actuelles.csv"'
        
        writer = csv.writer(response)
        writer.writerow(common_headers)
        
        for demande in Demande.objects.filter(is_deleted=False):
            poste, shift = safe_get_user_info(demande)
            writer.writerow([
                demande.id,
                poste,
                shift,
                demande.created_at.strftime('%d/%m/%Y %H:%M'),
                demande.statut,
                calculate_time_elapsed(demande.created_at, demande.validated_at)
            ])
        return response

    elif data_type == "alertemains":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="alertes_maintenance_actuelles.csv"'
        
        writer = csv.writer(response)
        writer.writerow(common_headers)
        
        for alerte in Alertemain.objects.filter(is_deleted=False):
            poste, shift = safe_get_user_info(alerte)
            writer.writerow([
                alerte.id,
                poste,
                shift,
                alerte.created_at.strftime('%d/%m/%Y %H:%M'),
                alerte.statut,
                calculate_time_elapsed(alerte.created_at, alerte.validated_at)
            ])
        return response

    elif data_type == "alertequals":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="alertes_qualite_actuelles.csv"'
        
        writer = csv.writer(response)
        writer.writerow(common_headers)
        
        for alerte in Alertequal.objects.filter(is_deleted=False):
            poste, shift = safe_get_user_info(alerte)
            writer.writerow([
                alerte.id,
                poste,
                shift,
                alerte.created_at.strftime('%d/%m/%Y %H:%M'),
                alerte.statut,
                calculate_time_elapsed(alerte.created_at, alerte.validated_at)
            ])
        return response

    elif data_type == "alertechefs":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="alertes_chef_equipe_actuelles.csv"'
        
        writer = csv.writer(response)
        writer.writerow(common_headers)
        
        for alerte in Alertechef.objects.filter(is_deleted=False):
            poste, shift = safe_get_user_info(alerte)
            writer.writerow([
                alerte.id,
                poste,
                shift,
                alerte.created_at.strftime('%d/%m/%Y %H:%M'),
                alerte.statut,
                calculate_time_elapsed(alerte.created_at, alerte.validated_at)
            ])
        return response

    elif data_type == "postes":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="postes_actuels.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Poste', 'Rôle', 'Date création', 'Dernière connexion', 'Statut'])
        
        for user in User.objects.filter(is_deleted=False):
            writer.writerow([
                user.poste,
                user.role(),
                user.created_at.strftime('%d/%m/%Y %H:%M'),
                user.last_login.strftime('%d/%m/%Y %H:%M') if user.last_login else "Jamais",
                "Actif"
            ])
        return response

    else:
        return HttpResponse("Type d'export non valide", status=400)