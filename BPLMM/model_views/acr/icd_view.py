from ...models import *
from django.shortcuts import render, get_object_or_404 # type: ignore
from django.core.paginator import Paginator # type: ignore


# 
# 
# 
def temp_icds_by_group(request, temp_group_id):
    icds = ACR_GROUPS_ICDS_TEMP.objects.filter(TEMP_ACR_GROUPID=temp_group_id, is_approved=False).order_by('-created_at')
    return render(request, 'components/htmx-templates/icds-temp.html', {'temp_group_id': temp_group_id, 'icds': paginate(request, icds, 2)})


# 
# 
# 
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
