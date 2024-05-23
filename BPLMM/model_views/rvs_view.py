from ..forms import *
from ..models import *
from django.db.models import Q # type: ignore
from datetime import datetime
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..decorators import encoder_required, approver_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
#services
from ..services.rvs_service import ACR_GROUPS_RVS_SERVICE
#repositories
from ..repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY

acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())

@login_required
@encoder_required
def rvs_create_modal(request, group_id):
    template = 'components/acr/fieldsets/acr-rvs.html'
    form = SAVE_RVS_FORM(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            try:
                acr_groups_rvs = acr_groups_rvs_service.create_temp_modal(data, group_id, request)
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
@login_required
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
@login_required
def main_rvs_by_group(request, group_id):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), ACR_GROUPID=group_id)
    else:
        rvs = ACR_GROUPS_RVS.objects.filter(DESCRIPTION__icontains=desc_search_query, ACR_GROUPID=group_id)
    return render(request, 'components/htmx-templates/rvs-main.html', {'rvs': paginate(request, rvs, 2), 'group_id':group_id})


def set_rvs_rules(request, group_id, rvs_code):
    template = 'pages/acr/encoder/rvs-rules-create.html'
    if request.method == 'POST':
        form = SAVE_RVS_RULES(request.POST)
        print(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                acr_groups_rvs_service.create_temp_rvs_rules(data, group_id, rvs_code, request.user.username)  
                messages.success(request, 'RVS RULES has been saved successfully.')
                return render(request, template, {'form': form, 'group_id': group_id, 'rvs_code': rvs_code})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, template, {'form': form, 'group_id': group_id, 'rvs_code': rvs_code})
        else:
            messages.error(request, 'Please make sure all fields are filled out.')
            return render(request, template, {'form': form, 'group_id': group_id, 'rvs_code': rvs_code})
    else:
        return render(request, template, {'group_id': group_id, 'rvs_code': rvs_code})
    
def check_if_rvs_effdate_exist(request):
    eff_date = request.GET.get('EFF_DATE', '')
    temp_rule_exists = ACR_PERRVS_RULES_TEMP.objects.filter(EFF_DATE=eff_date).exists()
    main_rule_exists = ACR_PERRVS_RULES.objects.filter(EFF_DATE=eff_date).exists()
    return render(request, 'components/htmx-templates/check_rvs_rvs_eff_date_existence.html', {'temp_rules': temp_rule_exists, 'main_rules': main_rule_exists})

    

def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj