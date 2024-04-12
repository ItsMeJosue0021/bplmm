from django.contrib import admin
from .models import ACR_GROUPS, ACR_GROUPS_ICDS, ACR_GROUPS_RVS, ACR_PERRVS_RULES

# Register your models here.

admin.site.register(ACR_GROUPS)
admin.site.register(ACR_GROUPS_ICDS)
admin.site.register(ACR_GROUPS_RVS)
admin.site.register(ACR_PERRVS_RULES)
