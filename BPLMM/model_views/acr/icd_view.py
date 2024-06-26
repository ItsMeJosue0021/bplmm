from ...models import *
from ...forms import *
from datetime import datetime
from django.db.models import Q # type: ignore
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from django.shortcuts import render, get_object_or_404 # type: ignore

from django.contrib.auth.decorators import login_required # type: ignore

#services
from ...services.icd_service import ACR_GROUPS_ICD_SERVICE

#repositories
from ...repositories.icd_repository import ACR_GROUPS_ICD_REPOSITORY


GROUP_ICD_SERVICE = ACR_GROUPS_ICD_SERVICE(ACR_GROUPS_ICD_REPOSITORY())


# 
# 
#  
@login_required
def create_temp_icd_modal(request, group_id):
    TEMPLATE = 'components/acr/fieldsets/acr-icds.html'
    form = SAVE_ICD_FORM(request.POST or None)
    
    print(request.POST)
    print(form.errors.as_data())
    
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            try:
                GROUP_ICD_SERVICE.create_temp_modal(data, request.user.username, group_id)
                messages.success(request, 'ICD has been successfully added.')
                return render(request, TEMPLATE, {'form': form, 'group_id': group_id})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, TEMPLATE, {'form': form, 'group_id': group_id}) 
        else:
            messages.error(request, 'Please make sure all fields are filled out.')
            return render(request, TEMPLATE, {'form': form, 'group_id': group_id}) 
    else:
        return render(request, TEMPLATE, {'form': form, 'group_id': group_id})
    
# 
# 
# 
@login_required
def temp_icds_by_group(request, temp_group_id):
    icds = ACR_GROUPS_ICDS_TEMP.objects.filter(TEMP_ACR_GROUPID=temp_group_id, is_approved=False).order_by('-created_at')
    return render(request, 'components/htmx-templates/icds-temp-by-group.html', {'temp_group_id': temp_group_id, 'icds': paginate(request, icds, 2)})

# 
# 
# 
@login_required
def temp_icds_by_approved_group(request, group_id):
    icds = ACR_GROUPS_ICDS_TEMP.objects.filter(ACR_GROUPID=group_id, is_approved=False).order_by('-created_at')
    return render(request, 'components/htmx-templates/icds-temp-by-group.html', {'group_id': group_id, 'icds': paginate(request, icds, 2)})
     
# 
# 
# 
@login_required
def main_icds_by_group(request, group_id):
    desc_search_query = request.GET.get('description_search', '')
    date_search_query = request.GET.get('date_search', '')
    
    if date_search_query:
        date_search_query = datetime.strptime(date_search_query, '%Y-%m-%d').date()
        icds = ACR_GROUPS_ICDS.objects.filter(Q(END_DATE=date_search_query), ACR_GROUPID=group_id).order_by('-created_at')
    elif desc_search_query:
        icds = ACR_GROUPS_ICDS.objects.filter(ACR_GROUPID=group_id, DESCRIPTION__icontains=desc_search_query).order_by('-created_at')
    else:
        icds = ACR_GROUPS_ICDS.objects.filter(ACR_GROUPID=group_id).order_by('-created_at')
    return render(request, 'components/htmx-templates/icds-main-by-group.html', {'group_id': group_id, 'icds': paginate(request, icds, 2)})
# 
# 
# 
@login_required
def temp_icd_with_rules_details(request, icdcode):
    TEMPLATE = 'pages/acr/temp_icd_with_rules_details.html'
    
    icd = get_object_or_404(ACR_GROUPS_ICDS_TEMP, ICDCODE=icdcode)
    
    rules = ACR_PERICD_RULES_TEMP.objects.filter(ICDCODE=icdcode).order_by('-created_at')
    
    return render(request, TEMPLATE, {'icd': icd, 'rules': rules, 'temp_group_id': icd.TEMP_ACR_GROUPID})
   
   
# 
# 
# 
# def check_if_rvs_effdate_exist(request):
#     eff_date = request.GET.get('EFF_DATE', '')
#     temp_rule_exists = ACR_PERRVS_RULES_TEMP.objects.filter(EFF_DATE=eff_date).exists()
#     main_rule_exists = ACR_PERRVS_RULES.objects.filter(EFF_DATE=eff_date).exists()
#     return render(request, 'components/htmx-templates/check_rvs_rvs_eff_date_existence.html', {'temp_rules': temp_rule_exists, 'main_rules': main_rule_exists}) 

# 
# 
# 
@login_required
def check_if_icdcode_exists(request):
    code = request.GET.get('ICDCODE', None)
    icdcode = None
    icdcode_main = ACR_GROUPS_ICDS.objects.filter(ICDCODE=code).exists()
    icdcode_temp = ACR_GROUPS_ICDS_TEMP.objects.filter(ICDCODE=code).exists()
    if icdcode_main:
        icdcode = icdcode_main
    elif icdcode_temp:
        icdcode = icdcode_temp
    return render(request, 'components/htmx-templates/check_icdcode_existence.html', {'icdcode': icdcode})   

# 
# 
# 
def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj
