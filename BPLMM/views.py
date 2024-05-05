import random
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import SAVE_RVS_FORM, ACR_GROUPS_FORM
from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .decorators import encoder_required, approver_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
from .services import ACR_GROUPS_SERVICE, ACR_GROUPS_RVS_SERVICE, ACR_PERRVS_RULES_SERVICE
from .repositories import ACR_GROUPS_REPOSITORY, ACR_GROUPS_RVS_REPOSITORY, ACR_PERRVS_RULES_REPOSITORY
from .models import ACR_GROUPS, ACR_GROUPS_TEMP, ACR_GROUPS_RVS, ACR_PERRVS_RULES


def group_item(request):
    temp_search_query = request.GET.get('temp_search', '')
    groups = ACR_GROUPS_TEMP.objects.filter(DESCRIPTION__icontains=temp_search_query)
    return render(request, 'components/temp_group.html', {'groups': groups})

#-------------------------------------------------
# LOGIN
#-------------------------------------------------
def login(request):
    if request.method == 'POST':
        print(request.POST) #remove after testing
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('nag login')
            auth_login(request, user)
            if user.groups.filter(name='Encoder').exists():
                return redirect('acr')
            elif user.groups.filter(name='Approver').exists():
                return redirect('create_icds')
            else:
                auth_logout(request)
                print('nag logout')
                return redirect('login')  
        else:
            print('hindi nag login')
            return render(request, 'pages/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'pages/login.html')
    
    
#-------------------------------------------------
# LOGOUT
#-------------------------------------------------
def logout(request):
    auth_logout(request)
    print('nag logout')
    return redirect('login')


#-------------------------------------------------
# ACR
#-------------------------------------------------
def acr(request):
    return render(request, 'pages/acr/acr.html')

#-------------------------------------------------
# GROUPS
#-------------------------------------------------
@login_required
def groups(request):
    
    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

    data = ACR_GROUPS.objects.all()

    temp_search_query = request.GET.get('temp_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        temp_groups = ACR_GROUPS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query))
    else:
        temp_groups = ACR_GROUPS_TEMP.objects.filter(DESCRIPTION__icontains=temp_search_query)

    temp_data_paginator = Paginator(temp_groups, 8) 
    page_number = request.GET.get('page', 1)
    temp_data = temp_data_paginator.get_page(page_number)

    form = ACR_GROUPS_FORM(request.POST or None)
    context = {'data': data, 'temp_data': temp_data, 'form': form}

    if request.method == 'POST':
        if form.is_valid():
            try:
                acr_groups = acr_groups_service.create_temp(form, request)
                if acr_groups is not None:
                    messages.success(request, 'Form saved successfully.')
                    return render(request, 'pages/acr/encoder/group-list.html', context)
                else:
                    raise Exception('An error occurred while saving the form.')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please make sure all fields are filled out.')

    return render(request, 'pages/acr/encoder/group-list.html', context)

    # if request.method == 'POST':

    #     form = ACR_GROUPS_FORM(request.POST)
    #     if form.is_valid():
    #         try:
    #             acr_groups = acr_groups_service.create_temp(form, request)
    #             if acr_groups is not None:
    #                 messages.success(request, 'Form saved successfully.')
    #                 return render(request, 'pages/acr/encoder/group-list.html', {'data': data, 'temp_data': temp_data})
    #         except Exception as e:
    #             messages.error(request, 'An error occurred while saving the form.')
    #             return render(request, 'pages/acr/encoder/group-list.html', {'data': data, 'temp_data': temp_data})
    #     else:
    #         messages.error(request, 'Please make sure all fields are filled out.')
    #         return render(request, 'pages/acr/encoder/group-list.html', {'form': form, 'data': data, 'temp_data': temp_data})
        
    # return render(request, 'pages/acr/encoder/group-list.html', {'data': data, 'temp_data': temp_data})


#-------------------------------------------------
# CREATE RVS (with GROUP)
#-------------------------------------------------
# @encoder_required
@login_required
def rvs_create(request):

    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
    acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
    acr_perrvs_rules_service = ACR_PERRVS_RULES_SERVICE(ACR_PERRVS_RULES_REPOSITORY())

    if request.method == 'POST':

        print(request.POST) #remove after testing

        form = SAVE_RVS_FORM(request.POST)

        try:
            acr_groups = acr_groups_service.create(form)
            acr_groups_rvs = acr_groups_rvs_service.create(form, acr_groups)
            #acr_perrvs_rules = acr_perrvs_rules_service.create(form, acr_groups.ACR_GROUPID, acr_groups_rvs.RVSCODE)

            if acr_groups is not None and acr_groups_rvs is not None:  
                print("ACR_GROUPS created successfully") #remove after testing
                form = SAVE_RVS_FORM()
                return render(request, 'pages/acr/encoder/rvs-create.html', {'form': form})
            else:
                print("Form is not valid") #remove after testing
                print(form.errors) #remove after testing
                return render(request, 'pages/acr/encoder/rvs-create.html', {'form': form})
        
        except Exception as e:
            
            print(f"An error occurred: {e}") #remove after testing
            return render(request, 'pages/acr/encoder/rvs-create.html', {'error_message': str(e)})
    
    form = SAVE_RVS_FORM()
    return render(request, 'pages/acr/encoder/rvs-create.html', {'form': form})


#-------------------------------------------------
# GENERATE ACR GROUP ID
#-------------------------------------------------
def generate_acr_group_id():
    return 'CR' + str(random.randint(1000, 9999))


#-------------------------------------------------
# SHOW GROUP
#-------------------------------------------------
def groups_show(request):
    pass


#-------------------------------------------------
# EDIT GROUP
#-------------------------------------------------
def groups_edit(request, group_id):
    pass


#-------------------------------------------------
# DELETE GROUP
#-------------------------------------------------
def groups_delete(request, group_id):
    pass


#-------------------------------------------------
# CREATE RVS 
#-------------------------------------------------
def rvs(request):
    return render(request, 'pages/acr/encoder/rvs-list.html')


#-------------------------------------------------
# UPDATE RVS
#-------------------------------------------------
@login_required
def rvs_update(request):

    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
    acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
    acr_perrvs_rules_service = ACR_PERRVS_RULES_SERVICE(ACR_PERRVS_RULES_REPOSITORY())

    if request.method == 'POST':

        print(request.POST) #remove after testing

        form = SAVE_RVS_FORM(request.POST)

        try:
            acr_groups = acr_groups_service.create(form)
            acr_groups_rvs = acr_groups_rvs_service.create(form, acr_groups)
            #acr_perrvs_rules = acr_perrvs_rules_service.create(form, acr_groups.ACR_GROUPID, acr_groups_rvs.RVSCODE)

            if acr_groups is not None and acr_groups_rvs is not None:  
                print("ACR_GROUPS created successfully") #remove after testing
                form = SAVE_RVS_FORM()
                return render(request, 'pages/acr/encoder/create-rvs.html', {'form': form})
            else:
                print("Form is not valid") #remove after testing
                print(form.errors) #remove after testing
                return render(request, 'pages/acr/encoder/create-rvs.html', {'form': form})
        
        except Exception as e:
            
            print(f"An error occurred: {e}") #remove after testing
            return render(request, 'pages/acr/encoder/create-rvs.html', {'error_message': str(e)})
    
    form = SAVE_RVS_FORM()
    return render(request, 'pages/acr/encoder/create-rvs.html', {'form': form})


#-------------------------------------------------
# GENERATE ACR GROUP ID
#-------------------------------------------------
def generate_acr_group_id():
    return 'CR' + str(random.randint(1000, 9999))

#-------------------------------------------------
# SHOW RVS
#-------------------------------------------------
def rvs_show(request):
    pass

#-------------------------------------------------
# EDIT RVS 
#-------------------------------------------------
def rvs_edit(request):
    pass

#-------------------------------------------------
# DELETE RVS
#-------------------------------------------------
def rvs_delete(request):
    pass

def set_rvs_rules(request):
    return render(request, 'pages/acr/encoder/rvs-rules-create.html')


#-------------------------------------------------
# LIST OF ICDS 
#-------------------------------------------------
def icds(request):
    return render(request, 'pages/acr/encoder/icds-list.html')

#-------------------------------------------------
# CREATE ICDS
#-------------------------------------------------
# @approver_required
@login_required
def create_icds(request):
    return render(request, 'pages/acr/encoder/icds-create.html')

def set_icds_rules(request):
    return render(request, 'pages/acr/encoder/icds-rules-create.html')




#----------------------------------------------------------------------------------------------------------
# APPROVER'S VIEWS
#----------------------------------------------------------------------------------------------------------

def approver_groups(request):
    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

    data = ACR_GROUPS.objects.all()

    temp_search_query = request.GET.get('temp_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        temp_groups = ACR_GROUPS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query))
    else:
        temp_groups = ACR_GROUPS_TEMP.objects.filter(DESCRIPTION__icontains=temp_search_query)

    temp_data_paginator = Paginator(temp_groups, 8) 
    page_number = request.GET.get('page', 1)
    temp_data = temp_data_paginator.get_page(page_number)

    form = ACR_GROUPS_FORM(request.POST or None)
    context = {'data': data, 'temp_data': temp_data, 'form': form}

    if request.method == 'POST':
        if form.is_valid():
            try:
                acr_groups = acr_groups_service.create_temp(form, request)
                if acr_groups is not None:
                    messages.success(request, 'Form saved successfully.')
                    return render(request, 'pages/acr/approver/group-list.html', context)
                else:
                    raise Exception('An error occurred while saving the form.')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please make sure all fields are filled out.')

    return render(request, 'pages/acr/approver/group-list.html', context)




