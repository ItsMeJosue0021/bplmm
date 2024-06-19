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

# auth
from .services.auth_service import AUTH_SERVICE

#services
from .services.group_service import ACR_GROUPS_SERVICE
from .services.rvs_service import ACR_GROUPS_RVS_SERVICE

#repositories
from .repositories.group_repository import ACR_GROUPS_REPOSITORY
from .repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY

# 
# 
# LOGIN
def login(request):
    TEMPLATE = 'pages/login.html'
    ERROR_MESSAGE = 'Invalid login credentials.'
    
    if request.user.is_authenticated:
        return redirect('acr')
    
    if request.method == 'POST':
        try:
            user = AUTH_SERVICE.authenticate_user(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                AUTH_SERVICE.login_user(request, user)
                return redirect(AUTH_SERVICE.authenticated_redirect(user))
            else:
                raise Exception(ERROR_MESSAGE)
        except Exception:
            return render(request, TEMPLATE, {'error': ERROR_MESSAGE})
    else:
        return render(request, TEMPLATE)

#
#  
# LOGOUT
def logout(request):
    AUTH_SERVICE.logout_user(request)
    return redirect('login')

# 
# 
# USER INFORMATION
@login_required
def get_current_user(request):
    user = request.user
    return render(request, 'components/auth/user-info-preview.html', {'user': user})

# 
# 
# ACR
@login_required
def acr(request):
    code = request.GET.get('code', request.session.get('code', ''))
    filter = request.GET.get('filter', request.session.get('filter', ''))
    request.session['code'] = code
    request.session['filter'] = filter

    group = None
    main_rvs_single = None
    temp_rvs_single = None
    context = {}

    if filter == 'group':
        group = ACR_GROUPS.objects.filter(ACR_GROUPID=code).first()

    elif filter == 'rvs':
        main_rvs_single = ACR_GROUPS_RVS.objects.filter(RVSCODE=code).first()
        temp_rvs_single = ACR_GROUPS_RVS_TEMP.objects.filter(RVSCODE=code, is_approved=False, ACR_GROUPID__exact='').first()
        if main_rvs_single:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=main_rvs_single.ACR_GROUPID).first()
        elif temp_rvs_single:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=temp_rvs_single.ACR_GROUPID).first()

    elif filter == 'icd':
        main_icds = ACR_GROUPS_ICDS.objects.filter(ICDCODE=code).first()
        temp_icds = ACR_GROUPS_ICDS_TEMP.objects.filter(ICDCODE=code, is_approved=False).first()
        if main_icds:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=main_icds.ACR_GROUPID).first()
        elif temp_icds:
            group = ACR_GROUPS.objects.filter(ACR_GROUPID=temp_icds.ACR_GROUPID).first()

    if group:
        temp_rvs = ACR_GROUPS_RVS_TEMP.objects.filter(ACR_GROUPID=group.ACR_GROUPID, is_approved=False, ACR_GROUPID__exact='')
        main_rvs = ACR_GROUPS_RVS.objects.filter(ACR_GROUPID=group.ACR_GROUPID)

        temp_icds = ACR_GROUPS_ICDS_TEMP.objects.filter(ACR_GROUPID=group.ACR_GROUPID, is_approved=False)
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

# 
# 
# CREATE RVS 
def rvs(request):
    return render(request, 'pages/acr/encoder/rvs-list.html')

# 
# 
# LIST OF ICDS 
def icds(request):
    return render(request, 'pages/acr/encoder/icds-list.html')


# 
# APPROVER'S VIEWS
#----------------------------------------------------------------------------------------------------------
@login_required
def approver_groups(request):
    TEMPLATE = 'pages/acr/approver/group-list.html'
    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

    data = ACR_GROUPS.objects.all()

    temp_search_query = request.GET.get('temp_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        temp_groups = ACR_GROUPS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query)).order_by('-created_at')
    else:
        temp_groups = ACR_GROUPS_TEMP.objects.filter(DESCRIPTION__icontains=temp_search_query).order_by('-created_at')

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
                    return render(request, TEMPLATE, context)
                else:
                    raise Exception('An error occurred while saving the form.')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please make sure all fields are filled out.')

    return render(request, TEMPLATE, context)

# 
# 
# ----------------------------------Z BENEFITS' TEMPORARY URLS-------------------------------
@login_required
def z_benefits_home(request):
    return render(request, 'pages/z_benefits/home.html')

# 
# 
# ----------------------------------DRG'S TEMPORARY URLS-------------------------------
@login_required
def drg_home(request):
    return render(request, 'pages/drg/home.html')

# 
# 
# -------------------------------------- MOCK VIEWS ----------------------------------------
def rvs_codes(request):
    code_search_query = request.GET.get('code_search', '')
    codes = RVS_CODE_MOCK.objects.filter(CODE__icontains=code_search_query)
    return render(request, 'components/mocks/rvs-code.html', {'codes': codes})

# 
# 
# 
def spc_codes(request):
    code_search_query = request.GET.get('spc_code_search', '')
    codes = SPC_CODE_MOCK.objects.filter(CODE__icontains=code_search_query)
    return render(request, 'components/mocks/spc-code.html', {'codes': codes})

# 
# 
# 
def claim_validation_rules(request):
    validation_rules_query_search_query = request.GET.get('validation_rules_search', '')
    rules = CLAIM_VALIDATION_INFOS.objects.filter(CONTENT__icontains=validation_rules_query_search_query)
    return render(request, 'components/mocks/claim-validation-rules.html', {'rules': rules})
  
# 
#    
# 
def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj