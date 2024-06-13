from ...forms import *
from ...models import *
from django.db.models import Q # type: ignore
from datetime import datetime
from django.urls import reverse # type: ignore
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ...decorators import encoder_required, approver_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
#services
from ...services.rvs_service import ACR_GROUPS_RVS_SERVICE
#repositories
from ...repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY

acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())

# 
# 
# 
@login_required
@encoder_required
def rvs_create_modal(request, group_id):
    template = 'components/acr/fieldsets/acr-rvs.html'
    form = SAVE_RVS_FORM(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            try:
                acr_groups_rvs = acr_groups_rvs_service.create_temp_modal(data, request.user.username, group_id = group_id)
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

# 
# 
# 
@login_required
def rvs_rules_new_modal(request, temp_group_id):
    TEMPLATE = 'components/acr/new_rvs_rules_modal_form.html'
    
    if request.method == 'POST':
        form = SAVE_RVS_AND_RULES(request.POST or None)
        
        print(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            try:
                acr_groups_rvs_service.create_temp(data, username=request.user.username, temp_acr_groupid=temp_group_id)
                acr_groups_rvs_service.create_temp_rvs_rules(data, data['RVSCODE'], request.user.username, temp_acr_groupid=temp_group_id)
                messages.success(request, 'Form saved successfully.')
                return render(request, TEMPLATE, {'form': form})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, TEMPLATE, {'form': form})  
        else:
            messages.error(request, 'Please make sure all fields are filled out.')
            return render(request, TEMPLATE, {'form': form})
    return render(request, TEMPLATE, {'temp_acr_groupid': temp_group_id})

# 
# rvs/<str:group_id>/temp
# returns group related RVS from temporary table
@login_required
def temp_rvs_by_group(request, group_id):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), ACR_GROUPID=group_id, is_approved=False).order_by('-created_at')
    else:
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(DESCRIPTION__icontains=desc_search_query, ACR_GROUPID=group_id, is_approved=False).order_by('-created_at')
    return render(request, 'components/htmx-templates/rvs-temp.html', {'rvs': paginate(request, rvs, 2), 'group_id':group_id})

# 
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

# 
# 
# 
@login_required
def main_rvs(request):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query))
    else:
        rvs = ACR_GROUPS_RVS.objects.filter(DESCRIPTION__icontains=desc_search_query)
    return render(request, 'components/htmx-templates/rvs-main.html', {'rvs': paginate(request, rvs, 2), 'apvr': True})

# 
# 
# 
@login_required
def main_rvs_details(request, rvscode):
    TEMPLATE = 'pages/acr/main_rvs_details.html'
    try:
        rvs = get_object_or_404(ACR_GROUPS_RVS, RVSCODE=rvscode)
        group =  get_object_or_404(ACR_GROUPS, ACR_GROUPID=rvs.ACR_GROUPID)
        rules = ACR_PERRVS_RULES.objects.filter(RVSCODE=rvscode)
        return render(request, TEMPLATE, {'rvs': rvs, 'group': group, 'rules':rules})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('approver_approved_rvs_list')    

# 
# 
#   
@login_required 
def temp_rvs(request):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), is_approved=False, TEMP_ACR_GROUPID__exact='')
    else:
        rvs = ACR_GROUPS_RVS_TEMP.objects.filter(DESCRIPTION__icontains=desc_search_query, is_approved=False, TEMP_ACR_GROUPID__exact='')
    return render(request, 'components/htmx-templates/rvs-temp.html', {'rvs': paginate(request, rvs, 2), 'apvr':True})

# 
# 
# 
@login_required
def temp_rvs_details(request, rvscode):
    TEMPLATE = 'pages/acr/temp_rvs_details.html'
    try:
        rvs = get_object_or_404(ACR_GROUPS_RVS_TEMP, RVSCODE=rvscode)
        group = get_object_or_404(ACR_GROUPS, ACR_GROUPID=rvs.ACR_GROUPID)
        
        if request.method == 'POST':
            try:
                acr_groups_rvs_service.create_main(rvs, rvs.ACR_GROUPID)
                rvs.is_approved = True
                rvs.save()
                messages.success(request, 'RVS has been approved successfully.')
                return redirect('main_rvs_details', rvscode=rvscode)
            except Exception as e:
                messages.error(request, str(e))
                return render(request, TEMPLATE, {'rvs': rvs, 'group': group})
        return render(request, TEMPLATE, {'rvs': rvs, 'group': group})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('approver_pending_rvs_list')
    
# 
# 
# 
def temp_rvs_with_rules_details(request, rvscode, temp_group_id):
    TEMPLATE = 'pages/acr/rvs-temp-with-group-and-rules-details.html'
    try:
        rvs = get_object_or_404(ACR_GROUPS_RVS_TEMP, RVSCODE=rvscode)
        rules = None
        if rvs:
            rules = ACR_PERRVS_RULES_TEMP.objects.filter(RVSCODE=rvscode)
        
        return render(request, TEMPLATE, {'rvs': rvs, 'rules': rules, 'temp_group_id': temp_group_id})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('approver_pending_groups_list')
    
# 
# 
# 
def update_temp_rvs(request, rvscode):
    
    rvs = ACR_GROUPS_RVS_TEMP.objects.filter(RVSCODE=rvscode).first()
    form = UPDATE_RVS(request.POST)
    
    # this gets the page where the update request has been submitted from
    page_of_origin = request.GET.get('from', '')
        
    print(request.POST) # for debugging purposes
    
    if form.is_valid():
        data = form.cleaned_data
        try:
            rvs.RVSCODE = data['RVSCODE']
            rvs.DESCRIPTION = data['DESCRIPTION']
            rvs.RVU = data['RVU']
            rvs.EFF_DATE = data['EFF_DATE']
            rvs.END_DATE = data['END_DATE']
            rvs.save()
            
            messages.success(request, 'Succesfully updated.')
            return check_page_redirect_for_update_temp_rvs(page_of_origin, rvs)
            
        except Exception as e:
            messages.error(request, str(e))
            return check_page_redirect_for_update_temp_rvs(page_of_origin, rvs)
    else:
        messages.error(request, 'Something went wrong. Please try again.')
        return check_page_redirect_for_update_temp_rvs(page_of_origin, rvs)

# 
# 
# funcion for checking where to recdirect in the function update_temp_rvs to avoid redundancy
def check_page_redirect_for_update_temp_rvs(page_of_origin, rvs):
    if page_of_origin and page_of_origin == 'temp_rvs_details':
        return redirect('temp_rvs_details', rvscode=rvs.RVSCODE)
    else:
        return redirect('temp_rvs_with_rules_details', temp_group_id=rvs.TEMP_ACR_GROUPID, rvscode=rvs.RVSCODE)
# 
# 
# 
def update_temp_rvs_rules(request, rvscode):
    eff_date = request.GET.get('eff_date', '')
    rule  = ACR_PERRVS_RULES_TEMP.objects.filter(RVSCODE=rvscode, EFF_DATE=eff_date).first()
    form = UPDATE_RVS_RULES(request.POST)
    
    page_of_origin = request.GET.get('from', '')
    
    # print(request.POST) # for debugging purposes
    print(form.errors) # for debugging purposes
    
    if form.is_valid():
        data = form.cleaned_data
        try:
            acr_groups_rvs_service.update_temp_rvs_rules(rule, data)
            messages.success(request, 'Succesfully updated.')
            
            if page_of_origin and page_of_origin == 'temp_rvs_rules_details':
                url = reverse('temp_rvs_rules_details', args=[rvscode])
                parameter = '?eff_date=' + eff_date
                return redirect(url + parameter)
            else:
                return redirect('temp_rvs_with_rules_details', temp_group_id=rule.TEMP_ACR_GROUPID, rvscode=rule.RVSCODE) 
        except Exception as e:
            messages.error(request, str(e))
            if page_of_origin and page_of_origin == 'temp_rvs_rules_details':
                # return redirect('temp_rvs_rules_details', rvscode=rule.RVSCODE)
                url = reverse('temp_rvs_rules_details', args=[rvscode])
                parameter = '?eff_date=' + eff_date
                return redirect(url + parameter)
            else:
                return redirect('temp_rvs_with_rules_details', temp_group_id=rule.TEMP_ACR_GROUPID, rvscode=rule.RVSCODE)  
    else:
        messages.error(request, 'Something went wrong. Please try again.')
        if page_of_origin and page_of_origin == 'temp_rvs_rules_details':
            # return redirect('temp_rvs_rules_details', rvscode=rule.RVSCODE)
            url = reverse('temp_rvs_rules_details', args=[rvscode])
            parameter = '?eff_date=' + eff_date
            return redirect(url + parameter)
        else:
            return redirect('temp_rvs_with_rules_details', temp_group_id=rule.TEMP_ACR_GROUPID, rvscode=rule.RVSCODE) 
# 
# 
# 
@login_required
def set_rvs_rules(request, group_id, rvs_code):
    template = 'pages/acr/encoder/rvs-rules-create.html'
    if request.method == 'POST':
        form = SAVE_RVS_RULES(request.POST)
        print(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                acr_groups_rvs_service.create_temp_rvs_rules(data, rvs_code, request.user.username, group_id = group_id)  
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
    
# 
# 
# 
@login_required
def check_if_rvs_effdate_exist(request):
    eff_date = request.GET.get('EFF_DATE', '')
    temp_rule_exists = ACR_PERRVS_RULES_TEMP.objects.filter(EFF_DATE=eff_date).exists()
    main_rule_exists = ACR_PERRVS_RULES.objects.filter(EFF_DATE=eff_date).exists()
    return render(request, 'components/htmx-templates/check_rvs_rvs_eff_date_existence.html', {'temp_rules': temp_rule_exists, 'main_rules': main_rule_exists})

# 
# 
# 
@login_required
def approver_pending_rvs(request):
    template = 'pages/acr/approver/pending_rvs_list.html'
    return render(request, template)

# 
# 
#   
@login_required
def approver_approved_rvs(request):
    template = 'pages/acr/approver/approved_rvs_list.html'
    return render(request, template)

# 
# 
# 
def temp_rvs_rules_list(request):
    TEMPLATE = 'pages/acr/tem_rvs_rules_list.html'
    return render(request, TEMPLATE)


# 
# 
# 
def get_temp_rvs_rules(request):
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        rules = ACR_PERRVS_RULES_TEMP.objects.filter(Q(END_DATE=date_search_query) | Q(EFF_DATE=date_search_query), is_approved=False, TEMP_ACR_GROUPID__exact='')
    else:
        rules = ACR_PERRVS_RULES_TEMP.objects.filter(is_approved=False, TEMP_ACR_GROUPID__exact='')
    return render(request, 'components/htmx-templates/temp_rvs_rules.html', {'rules': rules})

# 
# 
# 
def temp_rvs_rules_details(request, rvscode):
    TEMPLATE = 'pages/acr/temp_rvs_rules_details.html'
    EFF_DATE = request.GET.get('eff_date', '')
    
    if request.method == 'POST':
        try:
            rule = get_object_or_404(ACR_PERRVS_RULES_TEMP, RVSCODE=rvscode, EFF_DATE=EFF_DATE)
            acr_groups_rvs_service.create_main_rvs_rules(data=rule, group_id=rule.ACR_GROUPID, rvs_code=rvscode)
            rule.is_approved = True
            rule.save()
            messages.success(request, 'RVS RULES has been saved successfully.')
            return redirect('temp_rvs_rules_list')
        except Exception as e:
            messages.error(request, str(e))
            # return redirect('temp_rvs_rules_details' , rvscode=rvscode, eff_date=EFF_DATE)
            url = reverse('temp_rvs_rules_details', args=[rvscode])
            parameter = '?eff_date=' + EFF_DATE
            return redirect(url + parameter)
    else:
        try:
            rule = get_object_or_404(ACR_PERRVS_RULES_TEMP, RVSCODE=rvscode, EFF_DATE=EFF_DATE)
            rvs = get_object_or_404(ACR_GROUPS_RVS, RVSCODE=rvscode)
            return render(request, TEMPLATE, {'rule': rule, 'rvs': rvs})
        except Exception as e:
            messages.error(request, str(e))
            return redirect('temp_rvs_rules_list')
# 
# 
# 
def temp_rvs_rules_count(request):
    count = ACR_PERRVS_RULES_TEMP.objects.filter(is_approved=False, TEMP_ACR_GROUPID__exact='').count()
    return render(request, 'components/htmx-templates/temp_rvs_rules_count.html', {'count': count})
# 
# 
# 
@login_required
def temp_rvs_count(request):
    count = ACR_GROUPS_RVS_TEMP.objects.filter(is_approved=False, TEMP_ACR_GROUPID__exact='').count()
    return render(request, 'components/htmx-templates/temp_rvs_count.html', {'count': count})

# 
# 
# 
@login_required
def temp_groups_count(request):
    count = ACR_GROUPS_TEMP.objects.filter(is_approved=False).count()
    return render(request, 'components/htmx-templates/temp_groups_count.html', {'count': count})


            
    
# 
# 
# 
def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj