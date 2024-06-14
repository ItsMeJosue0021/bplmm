from ...models import *
from django.shortcuts import render # type: ignore
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
def paginate(request, data, items_per_page):
    paginator = Paginator(data, items_per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj