from django.urls import path # type: ignore
from .model_views.group_view import *
from .model_views.rvs_view import *
from . import views

urlpatterns = [

    
    # Authentication URLs
    #-------------------------------------------------
        path('', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('user/', views.get_current_user),

    
    # ACR' URLs
    #-------------------------------------------------
        path('acr/', views.acr, name='acr'),
        
        path('acr/<str:group_id>/rvs/create', rvs_create_modal, name='rvs_create_modal'), 

    
    # Groups' URLs
    #-------------------------------------------------
        path('groups/', groups, name='groups'),
        path('groups/<int:id>/', groups_show, name="groups_show"),
        path('groups/<int:id>/edit', groups_edit, name="groups_edit"),
        path('groups/<int:id>/delete', groups_delete, name="groups_delete"),
        path('groups/<int:id>/approve', groups_approve, name="groups_approve"),
        path('groups/temporary', groups_temporary, name='groups_temporary'),
        path('groups/main', groups_main, name='groups_main'),
        
        # checks whether RVS or ICD exist in a GROUP
        path('groups/<str:group_id>/check-related', check_rvs_or_icd_exists, name='check_rvs_or_icd_exists'),


    # RVS' URLs
    #-------------------------------------------------
        path('groups/rvs/', views.rvs, name='rvs'),
        path('groups/<str:group_id>/rvs/', views.rvs_create, name='rvs_create'),
        path('groups/rvs/<int:id>/', views.rvs_show, name="rvs_show"),
        path('groups/rvs/<int:id>/edit', views.rvs_edit, name="rvs_edit"),
        path('groups/rvs/<int:id>/delete', views.rvs_delete, name="rvs_delete"),
        path('groups/<str:group_id>/rvs/set_rules', views.set_rvs_rules, name="set_rvs_rules"),

        # returns group related RVS from temporary table
        path('rvs/<str:group_id>/temp', views.temp_rvs_by_group, name='temp_rvs_by_group'),

        # returns group related RVS from main table
        path('rvs/<str:group_id>/main', views.main_rvs_by_group, name='main_rvs_by_group'),



    # ICDS' URLs
    #-------------------------------------------------
        path('groups/icds/', views.icds, name='icds'),
        path('groups/<str:group_id>/icds/', views.create_icds, name='icds_create'),
        path('groups/icds/set_rules', views.set_icds_rules, name="set_icds_rules"),



    # APPROVER'S URLs
    #-------------------------------------------------
        path('apvr/groups/', views.approver_groups, name='approver_groups'),


    # -------------------------------- MOCK URL ---------------------------------------
        path('rvs/codes/', views.rvs_codes),
        path('spc/codes/', views.spc_codes),
        path('claim-valitaions-rules/', views.claim_validation_rules),
        
    #----------------------------------------------------------------------------------
        path('groups/rvs/new/', groups_rvs_new, name='groups_rvs_new'),
        
        path('rvscode/existence-check', views.check_if_rvscode_exists, name='check_rvscode_existence')

]