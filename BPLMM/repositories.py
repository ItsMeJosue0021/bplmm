from .models import ACR_GROUPS, ACR_GROUPS_TEMP, ACR_GROUPS_RVS, ACR_PERRVS_RULES

class ACR_GROUPS_REPOSITORY:
    #-------------------------------------------------
    # fields for ACR_GROUPS_RVS
    #-------------------------------------------------
    def create_temp(self, data):
        acr_groups_temp = ACR_GROUPS_TEMP(**data)
        acr_groups_temp.save()
        return acr_groups_temp
    
    def update(self, data):
        acr_groups = ACR_GROUPS(**data)
        acr_groups.save()
        return acr_groups
    
class ACR_GROUPS_RVS_REPOSITORY:
    def create(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
    def update(self, data):
        acr_groups_rvs = ACR_GROUPS_RVS(**data)
        acr_groups_rvs.save()
        return acr_groups_rvs
    
class ACR_PERRVS_RULES_REPOSITORY:
    def create(self, data):
        acr_perrvs_rules = ACR_PERRVS_RULES(**data)
        acr_perrvs_rules.save()
        return acr_perrvs_rules
    
    def update(self, data):
        acr_perrvs_rules = ACR_PERRVS_RULES(**data)
        acr_perrvs_rules.save()
        return acr_perrvs_rules