from ...forms import *
from ...models import *
from datetime import datetime
from django.db.models import Q # type: ignore
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ...decorators import encoder_required, approver_required
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
#services
from ...services.group_service import ACR_GROUPS_SERVICE
from ...services.rvs_service import ACR_GROUPS_RVS_SERVICE
from ...services.icd_service import ACR_GROUPS_ICD_SERVICE
#repositories
from ...repositories.group_repository import ACR_GROUPS_REPOSITORY
from ...repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY
from ...repositories.icd_repository import ACR_GROUPS_ICD_REPOSITORY


GROUPS_SERVICE = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
GROUP_RVS_SERVICE = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
GROUP_ICD_SERVICE = ACR_GROUPS_ICD_SERVICE(ACR_GROUPS_ICD_REPOSITORY())

# 
# 
# 
@login_required
@encoder_required
def groups_rvs_new(request):
    TEMPLATE = 'pages/acr/encoder/new_group_rvs_rules.html'
    
    if request.method == 'POST':
        form = SAVE_GROUP_RVS_RULES(request.POST)

        print(request.POST) # testing
        if form.is_valid():
            data = form.cleaned_data
            try:
                group = GROUPS_SERVICE.create_temp(data, request)
                GROUP_RVS_SERVICE.create_temp(data, username=request.user.username, temp_acr_groupid=group.ID)
                GROUP_RVS_SERVICE.create_temp_rvs_rules(data, data['RVSCODE'], request.user.username, temp_acr_groupid=group.ID)
                messages.success(request, 'Form saved successfully.')
                return render(request, TEMPLATE, {'form': form})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, TEMPLATE, {'form': form})   
        else:
            messages.error(request, 'Please make sure all fields are filled out.')
            return render(request, TEMPLATE, {'form': form})
    return render(request, TEMPLATE)

# 
# 
# 
def groups_icd_new(request):
    TEMPLATE = 'pages/acr/encoder/new_groups_icd_rules.html'
    form = SAVE_GROUP_ICD_RULES_FORM(request.POST or None)
    
    print(request.POST) # testing
    
    if request.method == 'POST':
        if form.is_valid():
            data =  form.cleaned_data
            print(data) # testing
            try:
                group = GROUPS_SERVICE.create_temp(data, request)
                GROUP_ICD_SERVICE.create_temp(data, username=request.user.username, temp_acr_groupid=group.ID)
                GROUP_ICD_SERVICE.create_temp_icd_rules(data, data['ICDCODE'], request.user.username, temp_acr_groupid=group.ID)
                messages.success(request, 'Form saved successfully.')
                return render(request, TEMPLATE, {'form': form})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, TEMPLATE, {'form': form})
        else:
            messages.error(request, 'Please make sure all fields are filled out.')
            return render(request, TEMPLATE, {'form': form})
    else:
        return render(request, TEMPLATE)  

# 
# 
# 
@login_required
@encoder_required
def groups(request):
    
    # acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

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
                acr_groups = GROUPS_SERVICE.create_temp(form, request.user.username)
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
@login_required
def groups_approve(request, id):

    # acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

    temp_group = get_object_or_404(ACR_GROUPS_TEMP, ID=id)

    try:
        acr_group = GROUPS_SERVICE.create_main(temp_group)
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
@login_required
def groups_temporary(request):
    description_search = request.GET.get('description_search', '')
    date_search = request.GET.get('date_search', '')
    
    if date_search:
        date_search = datetime.strptime(date_search, '%Y-%m-%d').date()
        groups = ACR_GROUPS_TEMP.objects.filter(Q(END_DATE=date_search) | Q(EFF_DATE=date_search), ACTIVE='F').order_by('-ID')
    else:
        groups = ACR_GROUPS_TEMP.objects.filter(DESCRIPTION__icontains=description_search, ACTIVE='F').order_by('-ID')

    return render(request, 'components/htmx-templates/groups-temp.html', {'groups': paginate(request, groups, 10)})


# /groups/main
# this will return all the groups that are in main groups table, the ones that have been approved
# this url will support searching, by description and by start and end date
# returns ajax rendered template
@login_required
def groups_main(request):
    description_search = request.GET.get('description_search', '')
    date_search = request.GET.get('date_search', '')
    
    if date_search:
        date_search = datetime.strptime(date_search, '%Y-%m-%d').date()
        groups = ACR_GROUPS.objects.filter(Q(END_DATE=date_search) | Q(EFF_DATE=date_search)).order_by('-ACR_GROUPID')
    else:
        groups = ACR_GROUPS.objects.filter(DESCRIPTION__icontains=description_search).order_by('-ACR_GROUPID')

    return render(request, 'components/htmx-templates/groups-main.html', {'groups': paginate(request, groups, 10)})

# 
# 
# checks whether RVS or ICD exists in a GROUP
@login_required
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

# 
# 
# This is also the view that handles the approving of GROUP, RVS and RVS RULES
@login_required
def temp_group_rvs_rules_details(request, id):
    template = 'pages/acr/temp_group_rvs_rules_details.html'
        
    group = ACR_GROUPS_TEMP.objects.filter(ID=id).first() 
    # group.EFF_DATE = 
    rvs = ACR_GROUPS_RVS_TEMP.objects.filter(TEMP_ACR_GROUPID=id).first() 
    rule = None
    if rvs is not None:
        rule = ACR_PERRVS_RULES_TEMP.objects.filter(TEMP_ACR_GROUPID=id, RVSCODE=rvs.RVSCODE).first()
        
    context = { 'group': group, 'rvs': rvs, 'rule': rule }
    
    if request.POST:
        try:
            main_group = GROUPS_SERVICE.create_main(group)
            if main_group is not None:
                group.ACTIVE = 'T'
                group.is_approved = True
                group.save()
                GROUP_RVS_SERVICE.create_main(rvs, main_group.ACR_GROUPID)
                rvs.is_approved = True
                rvs.ACR_GROUPID = main_group.ACR_GROUPID
                rvs.save()
                GROUP_RVS_SERVICE.create_main_rvs_rules(rule, group_id=main_group.ACR_GROUPID, rvs_code=rvs.RVSCODE)
                rule.is_approved = True
                rvs.ACR_GROUPID = main_group.ACR_GROUPID
                rule.save()
                messages.success(request, 'Succesfully approved.')
                return redirect('main_groups_rvs_or_icd_rules_details', group_id=main_group.ACR_GROUPID)
        except Exception as e:
            messages.error(request, str(e))
            return render(request, template, context)   
    else: 
        return render(request, template, context)
 
# 
# Hanldes approving of Pending Group, RVS and RVS RULES
#   
@login_required
def temp_group_rvs_or_icd_rules_details(request, id):
    template = 'pages/acr/temp_group_rvs_rules_details.html'
        
    group = ACR_GROUPS_TEMP.objects.filter(ID=id).first() 
    rvs_list = ACR_GROUPS_RVS_TEMP.objects.filter(TEMP_ACR_GROUPID=id, is_approved=False) or None
    icds_list = ACR_GROUPS_ICDS_TEMP.objects.filter(TEMP_ACR_GROUPID=id, is_approved=False) or None
    rvs_rules = ACR_PERRVS_RULES_TEMP.objects.filter(TEMP_ACR_GROUPID=id)
    icd_rules = ACR_PERICD_RULES_TEMP.objects.filter(TEMP_ACR_GROUPID=id)
        
    context = { 'group': group, 'rvs': rvs_list, 'icds': icds_list }
    
    if request.POST:
        _method = request.POST.get('_method', 'POST')
        if _method == 'POST':
            try: 
                main_group = GROUPS_SERVICE.create_main(group)
                if main_group is not None:
                    group.ACTIVE = 'T'
                    group.is_approved = True
                    group.save() 
                    
                    if icds_list:
                        for icd in icds_list:
                            GROUP_ICD_SERVICE.create_main(icd, main_group.ACR_GROUPID)
                            icd.is_approved = True
                            icd.ACR_GROUPID = main_group.ACR_GROUPID
                            icd.save()
                            
                            for rule in icd_rules:
                                if rule.ICDCODE != icd.ICDCODE:
                                    continue
                                GROUP_ICD_SERVICE.create_main_icd_rules(rule, group_id=main_group.ACR_GROUPID, icdcode=icd.ICDCODE)
                                rule.is_approved = True
                                icd.ACR_GROUPID = main_group.ACR_GROUPID
                                rule.save()
                                
                    elif rvs_list:            
                        for rvs in rvs_list: 
                            GROUP_RVS_SERVICE.create_main(rvs, main_group.ACR_GROUPID)
                            rvs.is_approved = True
                            rvs.ACR_GROUPID = main_group.ACR_GROUPID
                            rvs.save()
                            
                            for rule in rvs_rules:
                                if rule.RVSCODE != rvs.RVSCODE:
                                    continue
                                GROUP_RVS_SERVICE.create_main_rvs_rules(rule, group_id=main_group.ACR_GROUPID, rvs_code=rvs.RVSCODE)
                                rule.is_approved = True
                                rvs.ACR_GROUPID = main_group.ACR_GROUPID
                                rule.save()
                    
                    messages.success(request, 'Succesfully approved.')
                    return redirect('main_groups_rvs_or_icd_rules_details', group_id=main_group.ACR_GROUPID)
            except Exception as e:
                messages.error(request, str(e))
                return render(request, template, context)  
            
        elif _method == 'PUT':
            form = UPDATE_GROUP(request.POST)
            print(request.POST)
            
            if form.is_valid():
                data = form.cleaned_data
                try:
                    GROUPS_SERVICE.update_temp(data, group)
                    messages.success(request, 'Succesfully updated.')
                    return redirect('temp_group_rvs_rules_details', id=id)
                except Exception as e:
                    messages.error(request, str(e))
                    return redirect('temp_group_rvs_rules_details', id=id)
            else:
                context = { 'group': group, 'rvs': rvs_list, 'icds': icds_list, 'form': form }
                return render(request, template, context)      
    else:
        return render(request, template, context)

# 
# 
# 
@login_required
def main_groups_rvs_or_icd_rules_details(request, group_id):
    template = 'pages/acr/main_group_rvs_rules_details.html'
    
    group = ACR_GROUPS.objects.filter(ACR_GROUPID=group_id).first() 
    rvs_list = ACR_GROUPS_RVS.objects.filter(ACR_GROUPID=group_id)
    rules = ACR_PERRVS_RULES.objects.filter(ACR_GROUPID=group_id)
            
    context = { 'group': group, 'rvs': rvs_list, 'rules': rules }
    return render(request, template, context)
    
# 
# 
# 
@login_required
def approver_approved_groups(request):
    template = 'pages/acr/approver/pending_group_list.html'
    # acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())

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

    return render(request, template, context)

# 
# 
# 
@login_required
def approver_pending_groups(request):
    template = 'pages/acr/approver/approved_group_list.html'
    
    temp_search_query = request.GET.get('temp_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        groups = ACR_GROUPS.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query)).order_by('-created_at')
    else:
        groups = ACR_GROUPS.objects.filter(DESCRIPTION__icontains=temp_search_query).order_by('-created_at')

    temp_data_paginator = Paginator(groups, 8) 
    page_number = request.GET.get('page', 1)
    temp_data = temp_data_paginator.get_page(page_number)
    
    context = {'groups': groups}

    return render(request, template, context)

# 
# 
# return all the rvs in the temporary table that is related in a group by temporary group id
@login_required
def temp_group_rvs(request, temp_group_id):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), TEMP_ACR_GROUPID=temp_group_id, is_approved=False).order_by('-created_at')
    else:
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(DESCRIPTION__icontains=desc_search_query, TEMP_ACR_GROUPID=temp_group_id, is_approved=False).order_by('-created_at')
    return render(request, 'components/htmx-templates/rvs-temp-with-group-and-rules.html', {'rvs': paginate(request, rvs, 2), 'temp_group_id':temp_group_id})

# 
# EDIT GROUP
#-------------------------------------------------
@login_required
def groups_edit(request, group_id):
    pass


#
# DELETE GROUP
#-------------------------------------------------
@login_required
def groups_delete(request, group_id):
    pass

# 
# 
# 
def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj


