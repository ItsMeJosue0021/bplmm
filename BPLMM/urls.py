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

    #-------------------------------------------------
    # RVS' URLs
    #-------------------------------------------------
    path('groups/rvs/', views.rvs, name='rvs'),
    path('groups/rvs/create/', views.rvs_create, name='rvs_create'),
    path('groups/rvs/<int:id>/', views.rvs_show, name="rvs_show"),
    path('groups/rvs/<int:id>/edit', views.rvs_edit, name="rvs_edit"),
    path('groups/rvs/<int:id>/delete', views.rvs_delete, name="rvs_delete"),
    path('groups/rvs/set_rules', views.set_rvs_rules, name="set_rvs_rules"),

    #-------------------------------------------------
    # ICDS' URLs
    #-------------------------------------------------
    path('groups/icds/', views.icds, name='icds'),
    path('groups/icds/create/', views.create_icds, name='icds_create'),
    path('groups/icds/set_rules', views.set_icds_rules, name="set_icds_rules"),


    #-------------------------------------------------
    # APPROVER'S URLs
    #-------------------------------------------------
    path('apvr/groups/', views.approver_groups, name='approver_groups'),

    path('groups/item/', views.group_item, name='group_item'),


    # -------------------------------- MOCK URL ---------------------------------------
    path('rvs/codes/', views.rvs_codes),
    path('spc/codes/', views.spc_codes),
    path('claim-valitaions-rules/', views.claim_validation_rules),

]