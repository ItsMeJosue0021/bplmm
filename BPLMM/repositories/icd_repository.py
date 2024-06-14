from ..models import *

class ACR_GROUPS_ICD_REPOSITORY:
    def create_main(self, data):
        acr_groups_icd = ACR_GROUPS_ICDS(**data)
        acr_groups_icd.save()
        return acr_groups_icd
    
    def create_temp(self, data):
        acr_groups_icd = ACR_GROUPS_ICDS_TEMP(**data)
        acr_groups_icd.save()
        return acr_groups_icd
    
    def update_main(self, data):
        acr_groups_icd = ACR_GROUPS_ICDS(**data)
        acr_groups_icd.save()
        return acr_groups_icd
    
    def update_temp(self, data):
        acr_groups_icd = ACR_GROUPS_ICDS_TEMP(**data)
        acr_groups_icd.save()
        return acr_groups_icd   
    
    def create_temp_icd_rules(self, data):
        acr_groups_icd = ACR_PERICD_RULES_TEMP(**data)
        acr_groups_icd.save()
        return acr_groups_icd
    
    def create_main_icd_rules(self, data):
        acr_groups_icd = ACR_PERICD_RULES(**data)
        acr_groups_icd.save()
        return acr_groups_icd