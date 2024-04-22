from django.contrib import admin # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from .models import ACR_GROUPS, ACR_GROUPS_ICDS, ACR_GROUPS_RVS, ACR_PERRVS_RULES, CustomUser
from .models import ACR_GROUPS_LOG, ACR_GROUPS_TEMP, ACR_GROUPS_ICDS_LOG, ACR_GROUPS_ICDS_TEMP, ACR_GROUPS_RVS_LOG, ACR_GROUPS_RVS_TEMP
from .models import ACR_PERRVS_RULES_LOG, ACR_PERRVS_RULES_TEMP, ACR_PERICD_RULES_LOG, ACR_PERICD_RULES_TEMP

# Register your models here.

admin.site.register(ACR_GROUPS)
admin.site.register(ACR_GROUPS_ICDS)
admin.site.register(ACR_GROUPS_RVS)
admin.site.register(ACR_PERRVS_RULES)
admin.site.register(ACR_GROUPS_LOG)
admin.site.register(ACR_GROUPS_TEMP)
admin.site.register(ACR_GROUPS_ICDS_LOG)
admin.site.register(ACR_GROUPS_ICDS_TEMP)
admin.site.register(ACR_GROUPS_RVS_LOG)
admin.site.register(ACR_GROUPS_RVS_TEMP)
admin.site.register(ACR_PERRVS_RULES_LOG)
admin.site.register(ACR_PERRVS_RULES_TEMP)
admin.site.register(ACR_PERICD_RULES_LOG)
admin.site.register(ACR_PERICD_RULES_TEMP)

class MyUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(get_user_model(), MyUserAdmin)
