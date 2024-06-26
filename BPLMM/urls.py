from django.urls import path # type: ignore
from .model_views.acr import group_view
from .model_views.acr import rvs_view
from .model_views.acr import icd_view
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
        # 
        # 
        path('acr/', views.acr, name='acr'),
        
        # 
        # 
        path('acr/<str:group_id>/rvs/create', rvs_view.rvs_create_modal, name='rvs_create_modal'), 

    # Groups' URLs
    #-------------------------------------------------
        # 
        # 
        path('acr/groups/', group_view.groups, name='groups'),
        
        # 
        # 
        path('acr/groups/<int:id>/edit', group_view.groups_edit, name="groups_edit"),
        
        # 
        # 
        path('acr/groups/<int:id>/delete', group_view.groups_delete, name="groups_delete"),
        
        # 
        # 
        path('acr/groups/<int:id>/approve', group_view.groups_approve, name="groups_approve"),
        
        # 
        # 
        path('acr/groups/temporary', group_view.groups_temporary, name='groups_temporary'),
        
        # 
        # 
        path('acr/groups/main', group_view.groups_main, name='groups_main'),
        
        # 
        # checks whether RVS or ICD exist in a GROUP
        path('groups/<str:group_id>/check-related', group_view.check_rvs_or_icd_exists, name='check_rvs_or_icd_exists'),
        
        # 
        # 
        path('acr/temp-group/<str:temp_group_id>/rvs/', group_view.temp_group_rvs, name="temp_group_rvs"),
        
        # 
        # URL for approver's pending group list
        path('acr/shrd/groups/temporary', group_view.approver_approved_groups, name='approver_pending_groups_list'),
        
        # 
        # URL for approver's approved group list
        path('acr/shrd/groups/main', group_view.approver_pending_groups, name='approver_approved_groups_list'),
        
        # 
        # details of a temporary/pending group, rvs and rules
        path('acr/shrd/groups/<int:id>/details', group_view.temp_group_rvs_or_icd_rules_details, name='temp_group_rvs_or_icd_rules_details'),
        
        # 
        # details of a main/approved group, rvs and rules
        path('acr/shrd/groups/<str:group_id>/details', group_view.main_groups_rvs_or_icd_rules_details, name='main_groups_rvs_or_icd_rules_details'),
        
        # 
        # Adding of new RVS and RVS RULES to a pending GROUP
        path('acr/groups/<str:temp_group_id>/rvs/create', rvs_view.rvs_rules_new_modal, name='rvs_rules_new_modal'),

    # RVS' URLs
    #-------------------------------------------------
        # 
        # 
        path('acr/groups/rvs/', views.rvs, name='rvs'),
        
        # 
        # path('groups/<str:group_id>/rvs/', views.rvs_create, name='rvs_create'),
        path('acr/groups/<str:group_id>/rvs/<str:rvs_code>/set_rules', rvs_view.set_rvs_rules, name="set_rvs_rules"),

        # 
        # returns group related RVS from temporary table
        path('acr/rvs/<str:group_id>/temp', rvs_view.temp_rvs_by_group, name='temp_rvs_by_group'),

        # 
        # returns group related RVS from main table
        path('acr/rvs/<str:group_id>/main', rvs_view.main_rvs_by_group, name='main_rvs_by_group'),
        
        # 
        # Checks if RVS code exists
        path('acr/rvs/check_eff_date_existence/', rvs_view.check_if_rvs_effdate_exist, name="check_if_rvs_effdate_exist"),
        
        
        # 
        # APPROVER'S RVS URLs
        path('acr/shrd/rvs/temporary', rvs_view.approver_pending_rvs, name='approver_pending_rvs_list'),
        
        # 
        # 
        path('acr/shrd/rvs/main', rvs_view.approver_approved_rvs, name='approver_approved_rvs_list'),
        
        # 
        # 
        path('acr/shrd/rvs-main', rvs_view.main_rvs, name='main_rvs'),
        
        # 
        # 
        path('acr/shrd/rvs-temp', rvs_view.temp_rvs, name='temp_rvs'),
        
        # 
        # 
        path('acr/shrd/rvs/main/<str:rvscode>/details', rvs_view.main_rvs_details, name='main_rvs_details'),
        
        # 
        # 
        path('acr/shrd/rvs/temp/<str:rvscode>/details', rvs_view.temp_rvs_details, name='temp_rvs_details'),
        
        # 
        # 
        path('acr/shrd/<str:temp_group_id>/rvs_w_rules/temp/<str:rvscode>/details', rvs_view.temp_rvs_with_rules_details, name='temp_rvs_with_rules_details'),
        
        # 
        # 
        path('rvs/temp/count/', rvs_view.temp_rvs_count, name='temp_rvs_count'),
        
        # 
        # 
        path('groups/temp/count/', rvs_view.temp_groups_count, name='temp_groups_count'),
        
        # 
        # 
        path('rvs-rules/temp/count/', rvs_view.temp_rvs_rules_count, name='temp_rvs_rules_count'),
        
        # 
        # 
        path('acr/shrd/rvs_rules/temporary', rvs_view.temp_rvs_rules_list, name='temp_rvs_rules_list'),
        
        # 
        # 
        path('acr/shrd/rvs_rules/<str:rvscode>/', rvs_view.temp_rvs_rules_details, name='temp_rvs_rules_details'),
        
        # 
        # 
        path('acr/get_rvs_rules/temp', rvs_view.get_temp_rvs_rules, name='get_temp_rvs_rules'),
        
        # 
        # 
        path('rvs/<str:rvscode>/update', rvs_view.update_temp_rvs, name="update_temp_rvs"),
        
        # 
        # 
        path('rvs/<str:rvscode>/rules/update', rvs_view.update_temp_rvs_rules, name="update_temp_rvs_rules"),

    
    # 
    # 
    # 
    # 
    # ICDS' URLs
    #-------------------------------------------------
    
        # 
        # 
        path('acr/groups/icds/', views.icds, name='icds'),
        
        # 
        # creating new group with icd and rules
        path('acr/groups/icds/create/', group_view.groups_icd_new, name='groups_icd_new'),
        
        # 
        # 
        path('acr/icd/<str:group_id>/create/', icd_view.create_temp_icd_modal, name='create_temp_icd_modal'),
        
        # 
        # 
        path('acr/<str:temp_group_id>/icds/temp/', icd_view.temp_icds_by_group, name='temp_icds_by_group'),
        
        # 
        # 
        path('acr/group/<str:group_id>/icds/temp/', icd_view.temp_icds_by_approved_group, name='temp_icds_by_approved_group'),
        
        # 
        # 
        path('acr/<str:group_id>/icds/main/', icd_view.main_icds_by_group, name='main_icds_by_group'),
        
        
        # 
        # 
        path('acr/icd/<str:icdcode>/rules/temp/', icd_view.temp_icd_with_rules_details, name='temp_icd_with_rules_details'),
       


    # 
    # 
    # 
    # 
    # 
    # -------------------------------- MOCK URL ---------------------------------------
        # 
        # 
        path('rvs/codes/', views.rvs_codes, name="rvs_codes"),
        
        # 
        # 
        path('spc/codes/', views.spc_codes, name='spc_codes'),
        
        # 
        # 
        path('claim-valitaions-rules/', views.claim_validation_rules, name="claim_validation_rules"),
        
    #----------------------------------------------------------------------------------
    
        # 
        # 
        path('acr/groups/rvs/new/', group_view.groups_rvs_new, name='groups_rvs_new'),
        
        # 
        # 
        path('rvscode/existence-check', rvs_view.check_if_rvscode_exists, name='check_rvscode_existence'),
        
        # 
        # 
        path('icdcode/existence-check', icd_view.check_if_icdcode_exists, name='check_if_icdcode_exists'),
        
        
    # Z BENEFITS URLs
    # ===============================================================================================
    
    # 
    # 
    path('zbenefits/', views.z_benefits_home, name='z_benefits_home'),
    
    # DRG URLs
    # ===============================================================================================
    
    # 
    # 
    path('drg/', views.drg_home, name='drg_home'),
    

]