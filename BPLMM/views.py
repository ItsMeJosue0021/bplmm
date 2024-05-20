import random
from django.db.models import Q # type: ignore
from datetime import datetime
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from .forms import SAVE_RVS_FORM, ACR_GROUPS_FORM, SAVE_RVS_RULES
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from .decorators import encoder_required, approver_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
from .models import ACR_GROUPS, ACR_GROUPS_TEMP, ACR_GROUPS_RVS, ACR_PERRVS_RULES, RVS_CODE_MOCK, SPC_CODE_MOCK
from .models import CLAIM_VALIDATION_INFOS, ACR_GROUPS_RVS_TEMP, ACR_GROUPS_ICDS_TEMP, ACR_GROUPS_ICDS

#services
from .services.group_service import ACR_GROUPS_SERVICE
from .services.rvs_service import ACR_GROUPS_RVS_SERVICE

#repositories
from .repositories.group_repository import ACR_GROUPS_REPOSITORY
from .repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY


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
                return redirect('approver_groups')
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
# USER INFORMATION
#-------------------------------------------------
def get_current_user(request):
    user = request.user
    return render(request, 'components/auth/user-info-preview.html', {'user': user})


#-------------------------------------------------
# ACR
#-------------------------------------------------

def acr(request):
    group_id_search = request.GET.get('group_id_search', request.session.get('group_id_search', ''))
    rvs_search = request.GET.get('rvs_search', request.session.get('rvs_search', ''))
    icd_search = request.GET.get('icd_search', request.session.get('icd_search', ''))

    # Store the search parameters in the session
    request.session['group_id_search'] = group_id_search
    request.session['rvs_search'] = rvs_search
    request.session['icd_search'] = icd_search

    group = None
    main_rvs_single = None
    temp_rvs_single = None
    context = {}

    if group_id_search:
        group = ACR_GROUPS.objects.filter(ACR_GROUPID=group_id_search).first()

    elif rvs_search:
        main_rvs_single = ACR_GROUPS_RVS.objects.filter(RVSCODE=rvs_search).first()
        temp_rvs_single = ACR_GROUPS_RVS_TEMP.objects.filter(RVSCODE=rvs_search).first()
        if main_rvs_single:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=main_rvs_single.ACR_GROUPID).first()
        elif temp_rvs_single:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=temp_rvs_single.ACR_GROUPID).first()

    elif icd_search:
        main_icds = ACR_GROUPS_ICDS.objects.filter(ICDCODE=icd_search).first()
        temp_icds = ACR_GROUPS_ICDS_TEMP.objects.filter(ICDCODE=icd_search).first()
        if main_icds:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=main_icds.ACR_GROUPID).first()
        elif temp_icds:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=temp_icds.ACR_GROUPID).first()

    if group:
        temp_rvs = ACR_GROUPS_RVS_TEMP.objects.filter(ACR_GROUPID=group.ACR_GROUPID)
        main_rvs = ACR_GROUPS_RVS.objects.filter(ACR_GROUPID=group.ACR_GROUPID)

        temp_icds = ACR_GROUPS_ICDS_TEMP.objects.filter(ACR_GROUPID=group.ACR_GROUPID)
        main_icds = ACR_GROUPS_ICDS.objects.filter(ACR_GROUPID=group.ACR_GROUPID)
        
        button = None

        if main_rvs or temp_rvs:
            button = 'rvs'
        elif main_icds or temp_icds:
            button = 'icd'
        else:
            button = None

        context = {
            'group': group, 
            'temp_rvs': temp_rvs, 
            'main_rvs': main_rvs, 
            'temp_icds': temp_icds, 
            'main_icds': main_icds, 
            'button': button, 
            'main_rvs_single': main_rvs_single, 
            'temp_rvs_single': temp_rvs_single
            }

    return render(request, 'pages/acr/acr.html', context)















#-------------------------------------------------
# CREATE RVS (with GROUP)
#-------------------------------------------------
# @encoder_required
@login_required
def rvs_create(request, group_id):
    acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
    form = SAVE_RVS_FORM(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            print(request.POST) #remove after testing

            try:
                acr_groups_rvs = acr_groups_rvs_service.create(form, group_id, request)

                if acr_groups_rvs is not None:  
                    form = SAVE_RVS_FORM()
                    messages.success(request, 'RVS has been saved successfully.')
                    return render(request, 'pages/acr/encoder/rvs-create.html', {'form': form, 'group_id': group_id})
                else:
                    raise Exception('An error occurred while saving RVS.')
            except Exception as e:
                messages.error(request, str(e))
        else:
             messages.error(request, 'Please make sure all fields are filled out.')
    return render(request, 'pages/acr/encoder/rvs-create.html', {'form': form, 'group_id': group_id})


def rvs_create_modal(request, group_id):
    template = 'components/acr/fieldsets/acr-rvs.html'
    acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
    form = SAVE_RVS_FORM(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            try:
                acr_groups_rvs = acr_groups_rvs_service.create_temp_modal(form, group_id, request)

                if acr_groups_rvs is not None:  
                    form = SAVE_RVS_FORM()
                    messages.success(request, 'RVS has been saved successfully.')
                    return render(request, template, {'form': form, 'group_id': group_id})
                else:
                    raise Exception('An error occurred while saving RVS.')
            except Exception as e:
                messages.error(request, str(e))
        else:
             messages.error(request, 'Please make sure all fields are filled out.')
    return render(request, template, {'form': form, 'group_id': group_id})

# rvs/<str:group_id>/temp
# returns group related RVS from temporary table
def temp_rvs_by_group(request, group_id):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), ACR_GROUPID=group_id).order_by('-created_at')
    else:
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(DESCRIPTION__icontains=desc_search_query, ACR_GROUPID=group_id).order_by('-created_at')
    # rvs = ACR_GROUPS_RVS_TEMP.objects.filter(ACR_GROUPID=group_id)
    return render(request, 'components/htmx-templates/rvs-temp.html', {'rvs': paginate(request, rvs, 2), 'group_id':group_id})

# rvs/<str:group_id>/main
# returns group related RVS from main table
def main_rvs_by_group(request, group_id):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), ACR_GROUPID=group_id)
    else:
        rvs = ACR_GROUPS_RVS.objects.filter(DESCRIPTION__icontains=desc_search_query, ACR_GROUPID=group_id)
    # rvs = ACR_GROUPS_RVS.objects.filter(ACR_GROUPID=group_id)
    return render(request, 'components/htmx-templates/rvs-main.html', {'rvs': paginate(request, rvs, 2), 'group_id':group_id})

#-------------------------------------------------
# GENERATE ACR GROUP ID
#-------------------------------------------------
def generate_acr_group_id():
    return 'CR' + str(random.randint(1000, 9999))



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

def set_rvs_rules(request, group_id):

    if request.method == 'POST':

        form = SAVE_RVS_RULES(request.POST)
        print(request.POST)
        return render(request, 'pages/acr/encoder/rvs-rules-create.html', {'form': form, 'group_id': group_id})

    else:
        return render(request, 'pages/acr/encoder/rvs-rules-create.html', {'group_id': group_id})


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
def create_icds(request, group_id):
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


# -------------------------------------- MOCK VIEWS ----------------------------------------
def rvs_codes(request):
    code_search_query = request.GET.get('code_search', '')
    codes = RVS_CODE_MOCK.objects.filter(CODE__icontains=code_search_query)
    return render(request, 'components/mocks/rvs-code.html', {'codes': codes})

def spc_codes(request):
    code_search_query = request.GET.get('spc_code_search', '')
    codes = SPC_CODE_MOCK.objects.filter(CODE__icontains=code_search_query)
    return render(request, 'components/mocks/spc-code.html', {'codes': codes})

def claim_validation_rules(request):
    validation_rules_query_search_query = request.GET.get('validation_rules_search', '')
    rules = CLAIM_VALIDATION_INFOS.objects.filter(CONTENT__icontains=validation_rules_query_search_query)
    return render(request, 'components/mocks/claim-validation-rules.html', {'rules': rules})


def check_if_rvscode_exists(request):
    code = request.GET.get('RVSCODE', None)
    rvscode = None
    rvscode_main = ACR_GROUPS_RVS.objects.filter(RVSCODE=code).exists()
    rvscode_temp = ACR_GROUPS_RVS_TEMP.objects.filter(RVSCODE=code).exists()
    if rvscode_main:
        rvscode = rvscode_main
    elif rvscode_temp:
        rvscode = rvscode_temp
    return render(request, 'components/check_rvscode_existence.html', {'rvscode': rvscode})
    
    
def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj