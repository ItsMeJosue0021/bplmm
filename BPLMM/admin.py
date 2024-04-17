from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import ACR_GROUPS, ACR_GROUPS_ICDS, ACR_GROUPS_RVS, ACR_PERRVS_RULES, CustomUser

# Register your models here.

admin.site.register(ACR_GROUPS)
admin.site.register(ACR_GROUPS_ICDS)
admin.site.register(ACR_GROUPS_RVS)
admin.site.register(ACR_PERRVS_RULES)

class MyUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(get_user_model(), MyUserAdmin)
