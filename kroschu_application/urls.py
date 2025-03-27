from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'kroschu_application'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register_view'),
    path('valider_demande/<int:demande_id>/', views.valider_demande, name='valider_demande'),
    path('valider_alerte_maintenance/<int:alertemain_id>/', views.valider_alerte_maintenance, name='valider_alerte_maintenance'),
    path('valider_alerte_chef/<int:alertechef_id>/', views.valider_alerte_chef, name='valider_alerte_chef'),
    path('valider_alerte_qualite/<int:alertequal_id>/', views.valider_alerte_qualite, name='valider_alerte_qualite'),
    path('tache/<int:tache_id>/signaler_terminee/', views.signaler_tache_terminee, name='signaler_tache_terminee'),
    path('login_view/', views.login_view, name='login_view'),
    path('operateur_dashboard/', views.operateur_dashboard, name='operateur_dashboard'),
    path('logistique_dashboard/', views.logistique_dashboard, name='logistique_dashboard'),
    path('maintenance_dashboard/', views.maintenance_dashboard, name='maintenance_dashboard'),
    path('qualite_dashboard/', views.qualite_dashboard, name='qualite_dashboard'),
    path('chef_equipe_dashboard/', views.chef_equipe_dashboard, name='chef_equipe_dashboard'),
    path('demande_materiel/', views.demande_materiel, name='demande_materiel'),
    path('alerte_maintenance/', views.alerte_maintenance, name='alerte_maintenance'),
    path('alerte_qualite/', views.alerte_qualite, name='alerte_qualite'),
    path('alerte_chef/', views.alerte_chef, name='alerte_chef'),
    path('affecter_tache/', views.affecter_tache, name='affecter_tache'),
    path('signaler_tache_terminee/<int:tache_id>/', views.signaler_tache_terminee, name='signaler_tache_terminee'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('add_poste/', views.add_poste, name='add_poste'),

    path('soft_deleteposte/<str:model_name>/<str:poste>/', views.soft_deleteposte, name='soft_deleteposte'),
    path('soft_deletedem/<str:model_name>/<int:id>/', views.soft_deletedem, name='soft_deletedem'),

    

    path('admin_postes/', views.admin_postes, name='admin_postes'),
    path('admin_demandes/', views.admin_demandes, name='admin_demandes'),
    path('admin_dashboard/alertes_maintenance/', views.admin_alertes_maintenance, name='admin_alertes_maintenance'),
    path('admin_dashboard/alertes_qualite/', views.admin_alertes_qualite, name='admin_alertes_qualite'),
    path('admin_dashboard/alertes_chef/', views.admin_alertes_chef, name='admin_alertes_chef'),

   
    path('export_data/', views.export_data, name='export_data'),
    
]
