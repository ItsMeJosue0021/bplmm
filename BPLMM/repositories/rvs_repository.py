from ..models import *
    
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
        acr_groups_rvs = ACR_PERRVS_RULES(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
    def create_temp_rvs_rules(self, data):
        acr_groups_rvs = ACR_PERRVS_RULES_TEMP(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    