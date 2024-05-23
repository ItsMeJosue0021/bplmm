from ..forms import *
from ..models import *
from datetime import datetime
from django.db.models import Q # type: ignore
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..decorators import encoder_required, approver_required
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
#services
from ..services.group_service import ACR_GROUPS_SERVICE
from ..services.rvs_service import ACR_GROUPS_RVS_SERVICE
#repositories
from ..repositories.group_repository import ACR_GROUPS_REPOSITORY
from ..repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY


acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())

exception_error_message = 'Something went wrong while trying to save'
please_try_again = 'Please try again.'

@login_required
@encoder_required
def groups_rvs_new(request):
    template = 'pages/acr/encoder/new_group_rvs_rules.html'
    
    if request.method == 'POST':
        form = SAVE_GROUP_RVS_RULES(request.POST)

        print(request.POST) # testing
        if form.is_valid():
            data = form.cleaned_data
            try:
                group = acr_groups_service.create_temp(data, request)
                acr_groups_rvs_service.create_temp(data, group.ACR_GROUPID, request)
                acr_groups_rvs_service.create_temp_rvs_rules(data, group.ACR_GROUPID, data['RVSCODE'], request.user.username)
                messages.success(request, 'Form saved successfully.')
                return render(request, template, {'form': form})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, template, {'form': form})   
        else:
            messages.error(request, 'Please make sure all fields are filled out.')
            return render(request, template, {'form': form})
    return render(request, template)

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

    return render(request, 'components/htmx-templates/groups-temp.html', {'groups': paginate(request, groups, 2)})


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

    return render(request, 'components/htmx-templates/groups-main.html', {'groups': paginate(request, groups, 2)})


# checks whether RVS or ICD exists in a GROUP
def check_rvs_or_icd_exists(request, group_id):

    # group = ACR_GROUPS.objects.filter(ACR_GROUPID=group_id).first()
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

    return render(request, 'components/htmx-templates/rvs-icd-buttons.html', {'button': button, 'group_id': group_id})

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

def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


