from ..models import ACR_GROUPS, ACR_GROUPS_TEMP
from django.core.exceptions import ObjectDoesNotExist # type: ignore

class ACR_GROUPS_REPOSITORY:
    def create_main(self, data):
        acr_groups = ACR_GROUPS(**data)
        acr_groups.save()
        return acr_groups

    def create_temp(self, data):
        acr_groups_temp = ACR_GROUPS_TEMP(**data)
        acr_groups_temp.save()
        return acr_groups_temp
    
    def get_most_recent_groupid(self):
        try:
            return ACR_GROUPS.objects.latest('created_at').ACR_GROUPID
        except ObjectDoesNotExist:
            return None