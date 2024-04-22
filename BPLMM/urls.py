from django.urls import path # type: ignore
from . import views

urlpatterns = [

    #-------------------------------------------------
    # Authentication URLs
    #-------------------------------------------------
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    #-------------------------------------------------
    # Groups' URLs
    #-------------------------------------------------
    path('groups/', views.groups, name='groups'),
    path('groups/create/', views.groups_create, name='groups_create'),
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

    #-------------------------------------------------
    # ICDS' URLs
    #-------------------------------------------------
    path('groups/icds/create/', views.create_icds, name='create_icds'),
]