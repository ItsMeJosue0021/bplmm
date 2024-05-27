from django.urls import path # type: ignore
from .model_views.acr import group_view
from .model_views.acr import rvs_view
from . import views

urlpatterns = [

    # Authentication URLs
    #-------------------------------------------------
        path('', views.login, name='login'),
        path('logout/', views.logout, name='logout'),
        path('user/', views.get_current_user),
    
    # URLs FOR ALL CASE RATE (ACR)
    # =================================================================================================

    # ACR' URLs
    #-------------------------------------------------
        path('acr/', views.acr, name='acr'),
        
        path('acr/<str:group_id>/rvs/create', rvs_view.rvs_create_modal, name='rvs_create_modal'), 

    # Groups' URLs
    #-------------------------------------------------
        path('acr/groups/', group_view.groups, name='groups'),
        path('acr/groups/<int:id>/edit', group_view.groups_edit, name="groups_edit"),
        path('acr/groups/<int:id>/delete', group_view.groups_delete, name="groups_delete"),
        path('acr/groups/<int:id>/approve', group_view.groups_approve, name="groups_approve"),
        path('acr/groups/temporary', group_view.groups_temporary, name='groups_temporary'),
        path('acr/groups/main', group_view.groups_main, name='groups_main'),
        
        # checks whether RVS or ICD exist in a GROUP
        path('groups/<str:group_id>/check-related', group_view.check_rvs_or_icd_exists, name='check_rvs_or_icd_exists'),
        
     # APPROVER'S GROUP URLs
    #-------------------------------------------------
        # URL for approver's pending group list
        path('acr/apvr/groups/temporary', group_view.approver_approved_groups, name='approver_pending_groups_list'),
        # URL for approver's approved group list
        path('acr/apvr/groups/main', group_view.approver_pending_groups, name='approver_approved_groups_list'),
        # details of a temporary/pending group, rvs and rules
        path('acr/apvr/groups/<int:id>/details', group_view.temp_group_rvs_rules_details, name='temp_group_rvs_rules_details'),
        # details of a main/approved group, rvs and rules
        path('acr/apvr/groups/<str:group_id>/details', group_view.main_groups_rvs_rules_details, name='main_groups_rvs_rules_details'),

    # RVS' URLs
    #-------------------------------------------------
        path('acr/groups/rvs/', views.rvs, name='rvs'),
        # path('groups/<str:group_id>/rvs/', views.rvs_create, name='rvs_create'),
        path('acr/groups/<str:group_id>/rvs/<str:rvs_code>/set_rules', rvs_view.set_rvs_rules, name="set_rvs_rules"),

        # returns group related RVS from temporary table
        path('acr/rvs/<str:group_id>/temp', rvs_view.temp_rvs_by_group, name='temp_rvs_by_group'),

        # returns group related RVS from main table
        path('acr/rvs/<str:group_id>/main', rvs_view.main_rvs_by_group, name='main_rvs_by_group'),
        
        # Checks if RVS code exists
        path('acr/rvs/check_eff_date_existence/', rvs_view.check_if_rvs_effdate_exist, name="check_if_rvs_effdate_exist"),
        
        
        # APPROVER'S RVS URLs
        path('acr/apvr/rvs/temporary', rvs_view.approver_pending_rvs, name='approver_pending_rvs_list'),
        path('acr/apvr/rvs/main', rvs_view.approver_approved_rvs, name='approver_approved_rvs_list'),
        
        path('acr/apvr/rvs-main', rvs_view.main_rvs, name='main_rvs'),
        path('acr/apvr/rvs-temp', rvs_view.temp_rvs, name='temp_rvs'),

    # ICDS' URLs
    #-------------------------------------------------
        path('groups/icds/', views.icds, name='icds'),


    # -------------------------------- MOCK URL ---------------------------------------
        path('rvs/codes/', views.rvs_codes),
        path('spc/codes/', views.spc_codes),
        path('claim-valitaions-rules/', views.claim_validation_rules),
        
    #----------------------------------------------------------------------------------
        path('acr/groups/rvs/new/', group_view.groups_rvs_new, name='groups_rvs_new'),
        
        path('rvscode/existence-check', views.check_if_rvscode_exists, name='check_rvscode_existence'),
        
        
    # Z BENEFITS URLs
    # ===============================================================================================
    
    path('zbenefits/', views.z_benefits_home, name='z_benefits_home'),
    
    # DRG URLs
    # ===============================================================================================
    path('drg/', views.drg_home, name='drg_home'),
    

]