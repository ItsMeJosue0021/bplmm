from django.urls import path # type: ignore
from . import views

urlpatterns = [

    #-------------------------------------------------
    # Authentication URLs
    #-------------------------------------------------
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.get_current_user),

    #-------------------------------------------------
    # ACR' URLs
    #-------------------------------------------------
    path('acr/', views.acr, name='acr'),

    #-------------------------------------------------
    # Groups' URLs
    #-------------------------------------------------
    path('groups/', views.groups, name='groups'),
    # path('groups/create/', views.groups_create, name='groups_create'),
    path('groups/<int:id>/', views.groups_show, name="groups_show"),
    path('groups/<int:id>/edit', views.groups_edit, name="groups_edit"),
    path('groups/<int:id>/delete', views.groups_delete, name="groups_delete"),
    path('groups/<int:id>/approve', views.groups_approve, name="groups_approve"),
    path('groups/temporary', views.groups_temporary, name='groups_temporary'),
    path('groups/main', views.groups_main, name='groups_main'),

    #-------------------------------------------------
    # RVS' URLs
    #-------------------------------------------------
    path('groups/rvs/', views.rvs, name='rvs'),
    path('groups/<str:group_id>/rvs/', views.rvs_create, name='rvs_create'),
    # path('groups/rvs/', views.rvs_create, name='rvs_create'),
    path('groups/rvs/<int:id>/', views.rvs_show, name="rvs_show"),
    path('groups/rvs/<int:id>/edit', views.rvs_edit, name="rvs_edit"),
    path('groups/rvs/<int:id>/delete', views.rvs_delete, name="rvs_delete"),
    path('groups/rvs/set_rules', views.set_rvs_rules, name="set_rvs_rules"),

    # returns group related RVS from temporary table
    path('rvs/<str:group_id>/temp', views.temp_rvs_by_group, name='temp_rvs_by_group'),

    # returns group related RVS from main table
    path('rvs/<str:group_id>/main', views.main_rvs_by_group, name='temp_rvs_by_group'),


    #-------------------------------------------------
    # ICDS' URLs
    #-------------------------------------------------
    path('groups/icds/', views.icds, name='icds'),
    path('groups/<str:group_id>/icds/', views.create_icds, name='icds_create'),
    path('groups/icds/set_rules', views.set_icds_rules, name="set_icds_rules"),


    #-------------------------------------------------
    # APPROVER'S URLs
    #-------------------------------------------------
    path('apvr/groups/', views.approver_groups, name='approver_groups'),


    # -------------------------------- MOCK URL ---------------------------------------
    path('rvs/codes/', views.rvs_codes),
    path('spc/codes/', views.spc_codes),
    path('claim-valitaions-rules/', views.claim_validation_rules),

]