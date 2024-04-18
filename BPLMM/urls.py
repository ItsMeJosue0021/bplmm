from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('groups/', views.groups, name='groups'),
    path('rvs/create/', views.create_rvs, name='create_rvs'),
    path('icds/create/', views.create_icds, name='create_icds'),
]