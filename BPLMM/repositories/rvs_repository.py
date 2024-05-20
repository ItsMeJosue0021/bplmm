from ..models import ACR_GROUPS_RVS, ACR_GROUPS_RVS_TEMP
    
class ACR_GROUPS_RVS_REPOSITORY:
    def create_main(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
    def create_temp(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS_TEMP(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
    def update(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
    def create_main_rvs_rules(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
    def create_temp_rvs_rules(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS_TEMP(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    