from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Demande, Alertemain, Alertequal, Alertechef, Tache, Wire, Machine
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.db.models import Case, When, IntegerField
from django.utils import timezone
from django.utils.timezone import now
import csv
from django.http import HttpResponse
from .machine_mapping import get_compatible_machines

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        poste = request.POST['poste']
        role = request.POST['role']
        password = request.POST['password']
        new_user = User(poste=poste, role=role, password=make_password(password))
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
            if user.is_superuser:
                return redirect('kroschu_application:admin_postes')
            elif user.role == 'operateur':
                return redirect('kroschu_application:operateur_dashboard')
            elif user.role == 'logistique_incomming':
                return redirect('kroschu_application:logistique_dashboard')
            elif user.role == 'logistique_pagoda':
                return redirect('kroschu_application:logistique_dashboard')
            elif user.role == 'logistique_kit':
                return redirect('kroschu_application:logistique_dashboard')
            elif user.role == 'maintenance_board':
                return redirect('kroschu_application:maintenance_dashboard')
            elif user.role == 'maintenance_machine':
                return redirect('kroschu_application:maintenance_dashboard')
            elif user.role == 'qualite_vk':
                return redirect('kroschu_application:qualite_dashboard')
            elif user.role == 'qualite_cutting':
                return redirect('kroschu_application:qualite_dashboard')
            elif user.role == 'qualite_ksk':
                return redirect('kroschu_application:qualite_dashboard')
            elif user.role == 'chef_vk':
                return redirect('kroschu_application:chef_equipe_tasks')
            elif user.role == 'chef_cutting':
                return redirect('kroschu_application:chef_equipe_alerts')
            elif user.role == 'chef_ksk':
                return redirect('kroschu_application:chef_equipe_alerts')
            else:
                return redirect('kroschu_application:chef_equipe_alerts')
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
        return redirect('kroschu_application:home')
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
    taches = Tache.objects.filter(poste=poste, statut='en_attente')
    demandes = Demande.objects.filter(poste=poste, statut='en_attente')
    alertemains = Alertemain.objects.filter(poste=poste, statut='en_attente')
    alertequals = Alertequal.objects.filter(poste=poste, statut='en_attente')
    alertechefs = Alertechef.objects.filter(poste=poste, statut='en_attente')
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
    if request.method == "POST":
        logistique_type = request.POST.get('logistique_type')
        wire_ids = request.POST.getlist('wire_ids')
        demande = Demande.objects.create(
            poste=request.user,
            statut='en_attente',
            logistique_type=logistique_type
        )
        if wire_ids and logistique_type == 'logistique_pagoda':
            wires = Wire.objects.filter(id__in=wire_ids)
            if wires.exists():
                demande.wires.set(wires)
                demande.save()
        return redirect('kroschu_application:operateur_dashboard')
    return redirect('kroschu_application:operateur_dashboard')

@login_required
def alerte_maintenance(request):
    if request.method == 'POST':
        maintenance_type = request.POST.get('maintenance_type')
        Alertemain.objects.create(
            poste=request.user,
            statut='en_attente',
            maintenance_type=maintenance_type
        )
        return redirect('kroschu_application:operateur_dashboard')

@login_required
def alerte_chef(request):
    if request.method == 'POST':
        chef_type = request.POST.get('chef_type')
        if not chef_type:
            return redirect('kroschu_application:operateur_dashboard')
        Alertechef.objects.create(
            poste=request.user,
            statut='en_attente',
            chef_type=chef_type
        )
        return redirect('kroschu_application:operateur_dashboard')
    return render(request, 'chef_equipe_alerts.html')

@login_required
def alerte_qualite(request):
    if request.method == 'POST':
        qualite_type = request.POST.get('qualite_type')
        Alertequal.objects.create(
            poste=request.user,
            statut='en_attente',
            qualite_type=qualite_type
        )
        return redirect('kroschu_application:operateur_dashboard')

@login_required
def logistique_dashboard(request):
    role = request.user.role.lower()
    type_mapping = {
        'logistique_incomming': 'logistique_incomming',
        'logistique_pagoda': 'logistique_pagoda',
        'logistique_kit': 'logistique_kit'
    }
    logistique_type = type_mapping.get(role, None)
    zone_filter = request.GET.get('zone')
    # Filter Demande records by logistique_type and statut="en_attente"
    demandes = Demande.objects.filter(logistique_type=logistique_type, statut="en_attente")
    if zone_filter:
        demandes = demandes.filter(poste__zone=zone_filter)
    # Remove the ordering by statut since we only have "en_attente" records now
    demandes = demandes.order_by("created_at")
    concerne = {
        'logistique_incomming': 'logistique_incomming',
        'logistique_pagoda': 'logistique_pagoda',
        'logistique_kit': 'logistique_kit'
    }.get(role, 'LOGISTIQUE')
    context = {
        'demandes': demandes,
        'current_zone': zone_filter if zone_filter else 'Toutes zones',
        'logistique_type': concerne,
        'available_zones': ['VK', 'CUTTING', 'KSK']
    }
    return render(request, 'logistique_dashboard.html', context)

@login_required
def maintenance_dashboard(request):
    role = request.user.role.lower()
    type_mapping = {
        'maintenance_board': 'maintenance_board',
        'maintenance_machine': 'maintenance_machine',
    }
    maintenance_type = type_mapping.get(role, None)
    zone_filter = request.GET.get('zone')
    # Filter Alertemain records by maintenance_type and statut="en_attente"
    alertemains = Alertemain.objects.filter(maintenance_type=maintenance_type, statut="en_attente")
    if zone_filter:
        alertemains = alertemains.filter(poste__zone=zone_filter)
    # Remove the ordering by statut since we only have "en_attente" records now
    alertemains = alertemains.order_by("created_at")
    concerne = {
        'maintenance_board': 'maintenance_board',
        'maintenance_machine': 'maintenance_machine',
    }.get(role, 'MAINTENANCE')
    context = {
        'alertemains': alertemains,
        'current_zone': zone_filter if zone_filter else 'Toutes zones',
        'maintenance_type': concerne,
        'available_zones': ['VK', 'CUTTING', 'KSK']
    }
    return render(request, 'maintenance_dashboard.html', context)

@login_required
def qualite_dashboard(request):
    role = request.user.role.lower()
    type_mapping = {
        'qualite_vk': 'qualite_vk',
        'qualite_cutting': 'qualite_cutting',
        'qualite_ksk': 'qualite_ksk',
    }
    qualite_type = type_mapping.get(role, None)
    zone_filter = request.GET.get('zone')
    # Filter Alertequal records by qualite_type and statut="en_attente"
    alertequals = Alertequal.objects.filter(qualite_type=qualite_type, statut="en_attente")
    if zone_filter:
        alertequals = alertequals.filter(poste__zone=zone_filter)
    # Remove the ordering by statut since we only have "en_attente" records now
    alertequals = alertequals.order_by("created_at")
    concerne = {
        'qualite_vk': 'qualite_vk',
        'qualite_cutting': 'qualite_cutting',
        'qualite_ksk': 'qualite_ksk',
    }.get(role, 'Qualité')
    context = {
        'alertequals': alertequals,
        'current_zone': zone_filter if zone_filter else 'Toutes zones',
        'qualite_type': concerne,
        'available_zones': ['VK', 'CUTTING', 'KSK']
    }
    return render(request, 'qualite_dashboard.html', context)

@login_required
def chef_equipe_alerts(request):
    role = request.user.role.lower()
    type_mapping = {
        'chef_vk': 'chef_vk',
        'chef_cutting': 'chef_cutting',
        'chef_ksk': 'chef_ksk',
    }
    chef_type = type_mapping.get(role, None)
    if not chef_type:
        return redirect('kroschu_application:operateur_dashboard')

    zone_filter = request.GET.get('zone')
    # Filter Alertechef records by chef_type and statut="en_attente"
    alertechefs = Alertechef.objects.filter(chef_type=chef_type, statut="en_attente")
    if zone_filter and zone_filter in ['VK', 'CUTTING', 'KSK']:
        alertechefs = alertechefs.filter(poste__zone=zone_filter)
    else:
        zone_filter = None

    # Remove the ordering by statut since we only have "en_attente" records now
    alertechefs = alertechefs.order_by("created_at")
    concerne = {
        'chef_vk': 'chef_vk',
        'chef_cutting': 'chef_cutting',
        'chef_ksk': 'chef_ksk',
    }.get(role, 'CHEF')
    context = {
        'alertechefs': alertechefs,
        'current_zone': zone_filter if zone_filter else 'Toutes zones',
        'chef_type': concerne,
        'available_zones': ['VK', 'CUTTING', 'KSK']
    }
    return render(request, 'chef_equipe_alerts.html', context)

@login_required
def chef_equipe_tasks(request):
    if request.user.role != 'chef_vk':
        return redirect('kroschu_application:chef_equipe_alerts')
    
    zone_filter = request.GET.get('zone', 'VK')
    taches = Tache.objects.filter(statut='en_attente').order_by('created_at')
    
    # Récupérer le message de la session et le supprimer
    affect_message = request.session.pop('affect_message', None)
    
    context = {
        'taches': taches,
        'current_zone': zone_filter,
        'affect_message': affect_message  # Passer le message au template
    }
    return render(request, 'chef_equipe_tasks.html', context)

@login_required
def valider_demande(request, demande_id):
    try:
        demande = Demande.objects.get(id=demande_id)
        if demande.poste == request.user and demande.statut == 'en_attente':
            demande.statut = 'traité'
            demande.validated_at = now()
            demande.save()
        else:
            return redirect('kroschu_application:operateur_dashboard')
        return redirect('kroschu_application:operateur_dashboard')
    except Demande.DoesNotExist:
        return redirect('kroschu_application:operateur_dashboard')

@login_required
def affecter_tache(request):
    if request.user.role != 'chef_vk':
        return redirect('kroschu_application:home')

    if request.method == 'POST':
        ident_code = request.POST.get('ident_code', '').strip()

        if not ident_code:
            return redirect('kroschu_application:chef_equipe_tasks')

        ident_type = 'V_ident' if ident_code.startswith('V') else 'PM'
        wires = Wire.objects.filter(ident_code=ident_code)
        if not wires.exists():
            return redirect('kroschu_application:chef_equipe_tasks')

        version = wires.first().version
        compatible_machines = get_compatible_machines(ident_code)
        if not compatible_machines:
            return redirect('kroschu_application:chef_equipe_tasks')

        machines = Machine.objects.filter(name__in=compatible_machines)
        if not machines.exists():
            return redirect('kroschu_application:chef_equipe_tasks')

        # Priorité aux machines vides
        machine = machines.filter(is_occupied=False).first()
        if not machine:
            # Si toutes les machines sont occupées, rotation basée sur task_count
            machines = machines.order_by('task_count')
            machine = machines.first()

        if not machine or not machine.poste or machine.poste.role != 'operateur':
            return redirect('kroschu_application:chef_equipe_tasks')

        operateur = machine.poste
        tache = Tache.objects.create(
            poste=operateur,
            machine=machine,
            ident_type=ident_type,
            ident_code=ident_code,
            version=version,
            type_machine='soudage',
            statut='en_attente'
        )

        machine.is_occupied = True
        machine.current_task = tache
        machine.task_count += 1
        machine.save()

        # Message de confirmation
        request.session['affect_message'] = f"Tâche affectée à la machine {machine.name} (Poste {operateur.poste})"
        return redirect('kroschu_application:chef_equipe_tasks')

    return redirect('kroschu_application:chef_equipe_tasks')

@login_required
def signaler_tache_terminee(request, tache_id):
    try:
        tache = Tache.objects.get(id=tache_id)
        if tache.poste == request.user and tache.statut == 'en_attente':
            tache.statut = 'traité'
            tache.validated_at = now()
            if tache.machine:
                tache.machine.is_occupied = False
                tache.machine.current_task = None
                tache.machine.save()
            tache.save()
        else:
            return redirect('kroschu_application:operateur_dashboard')
    except Tache.DoesNotExist:
        return redirect('kroschu_application:operateur_dashboard')
    return redirect('kroschu_application:operateur_dashboard')

@login_required
def valider_alerte_maintenance(request, alertemain_id):
    try:
        alertemain = Alertemain.objects.get(id=alertemain_id)
        if alertemain.poste == request.user and alertemain.statut == 'en_attente':
            alertemain.statut = 'traité'
            alertemain.validated_at = now()
            alertemain.save()
        else:
            return redirect('kroschu_application:operateur_dashboard')
    except Alertemain.DoesNotExist:
        return redirect('kroschu_application:operateur_dashboard')
    return redirect('kroschu_application:operateur_dashboard')

@login_required
def valider_alerte_qualite(request, alertequal_id):
    try:
        alertequal = Alertequal.objects.get(id=alertequal_id)
        if alertequal.poste == request.user and alertequal.statut == 'en_attente':
            alertequal.statut = 'traité'
            alertequal.validated_at = now()
            alertequal.save()
        else:
            return redirect('kroschu_application:operateur_dashboard')
    except Alertequal.DoesNotExist:
        return redirect('kroschu_application:operateur_dashboard')
    return redirect('kroschu_application:operateur_dashboard')

@login_required
def valider_alerte_chef(request, alertechef_id):
    try:
        alertechef = Alertechef.objects.get(id=alertechef_id)
        if alertechef.poste == request.user and alertechef.statut == 'en_attente':
            alertechef.statut = 'traité'
            alertechef.validated_at = now()
            alertechef.save()
        else:
            return redirect('kroschu_application:operateur_dashboard')
    except Alertechef.DoesNotExist:
        return redirect('kroschu_application:operateur_dashboard')
    return redirect('kroschu_application:operateur_dashboard')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_poste(request):
    if request.method == 'POST':
        poste = request.POST['poste']
        role = request.POST['role']
        zone = request.POST['zone']
        password = request.POST['password']
        new_user = User(poste=poste, role=role, zone=zone, password=make_password(password))
        new_user.save()
        return redirect('kroschu_application:admin_postes')
    return render(request, 'admin_postes.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def soft_deleteposte(request, model_name, poste):
    models_map = {'user': User}
    model = models_map.get(model_name)
    if model:
        obj = get_object_or_404(model, poste=poste)
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
        model_class = globals()[model_info[0]]
        obj = get_object_or_404(model_class, id=id)
        obj.is_deleted = True
        obj.save()
        return redirect(model_info[1])
    return redirect('kroschu_application:admin_demandes')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_postes(request):
    postes = User.objects.filter(is_deleted=False)
    if request.method == 'POST':
        poste = request.POST.get('poste')
        zone = request.POST.get('zone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        User.objects.create_user(poste=poste, role=role, zone=zone, password=password)
        return redirect('kroschu_application:admin_postes')
    context = {'postes': postes}
    return render(request, 'admin_postes.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_demandes(request):
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
    context = {'demandes': demandes}
    return render(request, 'admin_demandes.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_alertes_maintenance(request):
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
    context = {'alertemains': alertemains}
    return render(request, 'admin_alertes_maintenance.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_alertes_qualite(request):
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
    context = {'alertequals': alertequals}
    return render(request, 'admin_alertes_qualite.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_alertes_chef(request):
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
    context = {'alertechefs': alertechefs}
    return render(request, 'admin_alertes_chef.html', context)

@login_required
def export_data(request):
    data_type = request.GET.get('type', '').lower()
    def safe_get_user_info(obj):
        if not hasattr(obj, 'poste') or obj.poste is None:
            return ("Inconnu", "N/A", "N/A")
        try:
            if obj.poste and not obj.poste.is_deleted:
                return (obj.poste.poste, obj.poste.shift, obj.poste.zone)
            return ("Utilisateur supprimé", "N/A", "N/A")
        except:
            return ("Erreur", "N/A", "N/A")
    def calculate_time_elapsed(created, validated):
        if not validated:
            return "En attente"
        try:
            delta = validated - created
            return f"{delta.total_seconds() / 60:.2f}"
        except Exception as e:
            print(f"Error calculating time: {e}")
            return "N/A"
    common_headers = ['ID', 'Poste', 'Shift', 'Zone', 'Date de création', 'Heure de création', 'Heure de clôture', 'Statut', 'Temps écoulé (min)']
    if data_type == "demandes":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="demandes_actuelles.csv"'
        writer = csv.writer(response)
        writer.writerow(common_headers)
        for demande in Demande.objects.filter(is_deleted=False):
            poste, shift, zone = safe_get_user_info(demande)
            writer.writerow([
                demande.id,
                poste,
                shift,
                zone,
                demande.created_at.strftime('%d/%m/%Y'),
                demande.created_at.strftime('%H:%M'),
                demande.validated_at.strftime('%H:%M') if demande.validated_at else "en_attente",
                demande.statut,
                calculate_time_elapsed(demande.created_at, demande.validated_at)
            ])
        return response
    elif data_type == "alertemains":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="alertes_maintenance_actuelles.csv"'
        writer = csv.writer(response)
        writer.writerow(common_headers)
        for alertemain in Alertemain.objects.filter(is_deleted=False):
            poste, shift, zone = safe_get_user_info(alertemain)
            writer.writerow([
                alertemain.id,
                poste,
                shift,
                zone,
                alertemain.created_at.strftime('%d/%m/%Y'),
                alertemain.created_at.strftime('%H:%M'),
                alertemain.validated_at.strftime('%H:%M') if alertemain.validated_at else "en_attente",
                alertemain.statut,
                calculate_time_elapsed(alertemain.created_at, alertemain.validated_at)
            ])
        return response
    elif data_type == "alertequals":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="alertes_qualite_actuelles.csv"'
        writer = csv.writer(response)
        writer.writerow(common_headers)
        for alertequal in Alertequal.objects.filter(is_deleted=False):
            poste, shift, zone = safe_get_user_info(alertequal)
            writer.writerow([
                alertequal.id,
                poste,
                shift,
                zone,
                alertequal.created_at.strftime('%d/%m/%Y'),
                alertequal.created_at.strftime('%H:%M'),
                alertequal.validated_at.strftime('%H:%M') if alertequal.validated_at else "en_attente",
                alertequal.statut,
                calculate_time_elapsed(alertequal.created_at, alertequal.validated_at)
            ])
        return response
    elif data_type == "alertechefs":
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="alertes_chef_equipe_actuelles.csv"'
        writer = csv.writer(response)
        writer.writerow(common_headers)
        for alertechef in Alertechef.objects.filter(is_deleted=False):
            poste, shift, zone = safe_get_user_info(alertechef)
            writer.writerow([
                alertechef.id,
                poste,
                shift,
                zone,
                alertechef.created_at.strftime('%d/%m/%Y'),
                alertechef.created_at.strftime('%H:%M'),
                alertechef.validated_at.strftime('%H:%M') if alertechef.validated_at else "en_attente",
                alertechef.statut,
                calculate_time_elapsed(alertechef.created_at, alertechef.validated_at)
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
                user.role,
                user.created_at.strftime('%d/%m/%Y %H:%M'),
                user.last_login.strftime('%d/%m/%Y %H:%M') if user.last_login else "Jamais",
                "Actif"
            ])
        return response
    else:
        return HttpResponse("Type d'export non valide", status=400)

@login_required
def view_task_details(request, task_id):
    try:
        tache = Tache.objects.get(id=task_id)
        # Vérifier les autorisations (seul l'opérateur assigné peut voir les détails)
        if request.user.role != 'operateur' or tache.poste != request.user:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)

        wires = Wire.objects.filter(ident_code=tache.ident_code, version=tache.version).values(
            'id', 'section', 'length', 'color', 'position', 'L_ident', 'version'
        )
        
        # Renommer L_ident en barcode pour correspondre au JavaScript
        wires_list = [
            {
                'id': wire['id'],
                'section': wire['section'],
                'length': wire['length'],
                'color': wire['color'],
                'position': wire['position'],
                'L_ident': wire['L_ident'],  # Renommé pour correspondre au JavaScript
                'version': wire['version']
            }
            for wire in wires
        ]

        return JsonResponse({
            'ident_code': tache.ident_code,
            'ident_type': tache.ident_type,
            'wires': wires_list
        })
    except Tache.DoesNotExist:
        return JsonResponse({'error': 'Tâche non trouvée'}, status=404)

@login_required
def demande_materiel_for_task(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id)
    if request.method == "POST":
        logistique_type = request.POST.get('logistique_type')
        wire_ids = request.POST.getlist('wire_ids')
        if not wire_ids:
            return JsonResponse({'error': 'Aucun fil sélectionné'}, status=400)
        demande = Demande.objects.create(
            poste=request.user,
            statut='en_attente',
            logistique_type=logistique_type
        )
        wires = Wire.objects.filter(id__in=wire_ids, ident_code=tache.ident_code)
        if wires.exists():
            demande.wires.set(wires)
            demande.save()
        return redirect('kroschu_application:operateur_dashboard')
    return redirect('kroschu_application:operateur_dashboard')