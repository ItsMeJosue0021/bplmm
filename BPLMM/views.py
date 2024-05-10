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
from .services import ACR_GROUPS_SERVICE, ACR_GROUPS_RVS_SERVICE, ACR_PERRVS_RULES_SERVICE
from .repositories import ACR_GROUPS_REPOSITORY, ACR_GROUPS_RVS_REPOSITORY, ACR_PERRVS_RULES_REPOSITORY
from .models import ACR_GROUPS, ACR_GROUPS_TEMP, ACR_GROUPS_RVS, ACR_PERRVS_RULES, RVS_CODE_MOCK, SPC_CODE_MOCK
from .models import CLAIM_VALIDATION_INFOS, ACR_GROUPS_RVS_TEMP, ACR_GROUPS_ICDS_TEMP, ACR_GROUPS_ICDS


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
    group_id_search = request.GET.get('group_id_search', '')
    rvs_search = request.GET.get('rvs_search', '')
    icd_search = request.GET.get('icd_search', '')

    group = None
    context = {}

    if group_id_search:
        group = ACR_GROUPS.objects.filter(ACR_GROUPID=group_id_search).first()

    elif rvs_search:
        main_rvs = ACR_GROUPS_RVS.objects.filter(RVSCODE=rvs_search).first()
        temp_rvs = ACR_GROUPS_RVS_TEMP.objects.filter(RVSCODE=rvs_search).first()
        if main_rvs:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=main_rvs.ACR_GROUPID).first()
        elif temp_rvs:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=temp_rvs.ACR_GROUPID).first()

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

        context = {'group': group, 'temp_rvs': temp_rvs, 'main_rvs': main_rvs, 'temp_icds': temp_icds, 'main_icds': main_icds}

    return render(request, 'pages/acr/acr.html', context)

















#-------------------------------------------------
# GROUPS
#-------------------------------------------------
@login_required
@encoder_required
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
                    form = SAVE_RVS_FORM()
                    messages.success(request, 'Form saved successfully.')
                    return render(request, 'pages/acr/encoder/group-list.html', {'data': data, 'temp_data': temp_data,'form': form})
                else:
                    raise Exception('An error occurred while saving the form.')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please make sure all fields are filled out.')

    return render(request, 'pages/acr/encoder/group-list.html', context)

# /groups/<int : id>/approve
# this will retrieve a group by id
# this will set the group's ACTIVE field to 'T' which represents True
# this will create new object in the ACR_GROUPS table by transfering the data of the group from ACR_GROUPS_TEMP table to the ACR_GROUPS table
# ACR_GROUPID = Get the most recent's objects ACR_GROUPID and increment it
# DESCRIPTION = ACR_GROUPS_TEMP.DESCRIPTION 
# EFF_DATE = ACR_GROUPS_TEMP.EFF_DATE
# ACTIVE = ACR_GROUPS_TEMP.ACTIVE 
# END_DATE = ACR_GROUPS_TEMP.END_DATE

def groups_approve(request, id):

    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

    temp_group = get_object_or_404(ACR_GROUPS_TEMP, ID=id)

    try:
        acr_group = acr_groups_service.create_main(temp_group)
        if acr_group is not None:
            messages.success(request, 'Group approved successfully.')
            temp_group.ACTIVE = 'T'
            temp_group.save()
            return redirect('approver_groups')
        else:
            raise Exception('An error occurred while approving the group.')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('approver_groups')


    # return redirect('approver_groups')

# /groups/temporary
# this will return all the groups that are in the temporary groups table
# this url will support searching, by description and by start and end date
# returns ajax rendered template

def groups_temporary(request):
    description_search = request.GET.get('description_search', '')
    date_search = request.GET.get('date_search', '')
    
    if date_search:
        date_search = datetime.strptime(date_search, '%Y-%m-%d').date()
        groups = ACR_GROUPS_TEMP.objects.filter(Q(END_DATE=date_search) | Q(EFF_DATE=date_search), ACTIVE='F').order_by('-ID')
    else:
        groups = ACR_GROUPS_TEMP.objects.filter(DESCRIPTION__icontains=description_search, ACTIVE='F').order_by('-ID')

    return render(request, 'components/htmx-rendered/groups-temp.html', {'groups': groups})


# /groups/main
# this will return all the groups that are in main groups table, the ones that have been approved
# this url will support searching, by description and by start and end date
# returns ajax rendered template
def groups_main(request):
    description_search = request.GET.get('description_search', '')
    date_search = request.GET.get('date_search', '')
    
    if date_search:
        date_search = datetime.strptime(date_search, '%Y-%m-%d').date()
        groups = ACR_GROUPS.objects.filter(Q(END_DATE=date_search) | Q(EFF_DATE=date_search)).order_by('-ACR_GROUPID')
    else:
        groups = ACR_GROUPS.objects.filter(DESCRIPTION__icontains=description_search).order_by('-ACR_GROUPID')

    return render(request, 'components/htmx-rendered/groups-main.html', {'groups': groups})


# checks whether RVS or ICD exists in a GROUP
def check_rvs_or_icd_exists(request, group_id):

    group = ACR_GROUPS.objects.filter(ACR_GROUPID=group_id).first()
    main_rvs = ACR_GROUPS_RVS.objects.filter(ACR_GROUPID=group_id)
    main_icds = ACR_GROUPS_ICDS.objects.filter(ACR_GROUPID=group_id)
    temp_rvs = ACR_GROUPS_RVS_TEMP.objects.filter(ACR_GROUPID=group_id)
    temp_icds = ACR_GROUPS_ICDS_TEMP.objects.filter(ACR_GROUPID=group_id)

    button = None

    if main_rvs or temp_rvs:
        button = 'rvs'
    elif main_icds or temp_icds:
        button = 'icd'
    else:
        button = None

    return render(request, 'components/htmx-rendered/rvs-icd-buttons.html', {'button': button, 'group_id': group_id})




























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


# rvs/<str:group_id>/temp
# returns group related RVS from temporary table
def temp_rvs_by_group(request, group_id):
    rvs = ACR_GROUPS_RVS_TEMP.objects.filter(ACR_GROUPID=group_id)
    return render(request, 'components/htmx-rendered/rvs-temp.html', {'rvs': rvs})

# rvs/<str:group_id>/main
# returns group related RVS from main table
def main_rvs_by_group(request, group_id):
    rvs = ACR_GROUPS_RVS.objects.filter(ACR_GROUPID=group_id)
    return render(request, 'components/htmx-rendered/rvs-main.html', {'rvs': rvs})

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



