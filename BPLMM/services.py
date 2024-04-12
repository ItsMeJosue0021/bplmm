import random
from .models import ACR_GROUPS, ACR_GROUPS_RVS

class ACR_GROUPS_SERVICE:

    def __init__(self, repository):
        self.repository = repository

    def create(self, form):
        if form.is_valid():
            data = form.cleaned_data
            acr_groups_data = {
                'ACR_GROUPID': self.generate_acr_group_id(),
                'DESCRIPTION': data['ACR_GROUPS_DESCRIPTION'],
                'EFF_DATE': data['GROUP_EFF_DATE'],
                'ACTIVE': 'F',
                'END_DATE': data['GROUP_END_DATE']
            }
            return self.repository.create(acr_groups_data)
        else:
            return None
        
    def generate_acr_group_id(self):
        return 'CR' + str(random.randint(1000, 9999))
    
class ACR_GROUPS_RVS_SERVICE:

    def __init__(self, repository):
        self.repository = repository

    def create(self, form, acr_groups):
        if form.is_valid():
            data = form.cleaned_data
            acr_groups_rvs_data = {
                'RVSCODE': self.generate_acr_group_rvs_id(),
                'ACR_GROUPID': acr_groups,
                'DESCRIPTION': data['ACR_GROUPS_RVS_DESCRIPTION'],
                'RVU': data['RVU'],
                'EFF_DATE': data['ACR_GROUPS_RVS_EFF_DATE'],
                'END_DATE': data['ACR_GROUPS_RVS_END_DATE']
            }
            return self.repository.create(acr_groups_rvs_data)
        else:
            return None
        
    def generate_acr_group_rvs_id(self):
        return 'RVS' + str(random.randint(1000, 9999))
        
class ACR_PERRVS_RULES_SERVICE:

    def __init__(self, repository):
        self.repository = repository

    def create(self, form, acr_groupid, rvscodes):
        if form.is_valid():
            data = form.cleaned_data
            acr_perrvs_rules_data = {
                'ACR_GROUPID': acr_groupid,
                'RVSCODE': rvscodes,
                'EFF_DATE': data['EFF_DATE'],
                'PRIMARY_AMOUNT': data['PRIMARY_HOSP_SHARE'] + data['PRIMARY_PROF_SHARE'],
                'PRIMARY_HOSP_SHARE': data['PRIMARY_HOSP_SHARE'],
                'PRIMARY_PROF_SHARE': data['PRIMARY_PROF_SHARE'],
                'SECONDARY_AMOUNT': data['SECONDARY_HOSP_SHARE'] + data['SECONDARY_PROF_SHARE'],
                'SECONDARY_HOSP_SHARE': data['SECONDARY_HOSP_SHARE'],
                'SECONDARY_PROF_SHARE': data['SECONDARY_PROF_SHARE'],
                'PCF_AMOUNT': data['PCF_AMOUNT'],
                'PCF_HOSP_SHARE': data['PCF_HOSP_SHARE'],
                'PCF_PROF_SHARE': data['PCF_PROF_SHARE'],
                'CHECK_OCCURS_PER_CLAIM': data['CHECK_OCCURS_PER_CLAIM'],
                'CHECK_OCCURS_PER_PERSON': data['CHECK_OCCURS_PER_PERSON'],
                'CHECK_LATERALITY': data['HECK_LATERALITY'],
                'CHECK_GENDER': data['CHECK_GENDER'],
                'CHECK_AGE': '18y-59.999y', # temporarily filled with mock data | data['CHECK_AGE']
                'CHECK_FACILITY_H1': data['CHECK_FACILITY_H1'],
                'CHECK_FACILITY_H2': data['CHECK_FACILITY_H2'],
                'CHECK_FACILITY_H3': data['CHECK_FACILITY_H3'],
                'CHECK_FACILITY_ASC': data['CHECK_FACILITY_ASC'],
                'CHECK_FACILITY_PCF': data['CHECK_FACILITY_PCF'],
                'CHECK_FACILITY_MAT': data['CHECK_FACILITY_MAT'],
                'CHECK_FACILITY_FSDC': data['CHECK_FACILITY_FSDC'],
                'CHECK_SINGLE_PERIOD_DAYS': data['CHECK_SINGLE_PERIOD_DAYS'],
                'CHECK_ADDITIONAL_CODES': 'CR4550 CR4551' , # temporarily filled with mock data | data['CHECK_ADDITIONAL_CODES']
                'CHECK_PREAUTHORIZATION': data['CHECK_PREAUTHORIZATION'],
                'CHECK_QUALIFIER': data['CHECK_QUALIFIER'],
                'DEDUCT_FROM_45DAYS': '1 DAY PER 4 SESSIONS', # temporarily filled with mock data | data['DEDUCT_FROM_45DAYS']
                'CHECK_GIDAS': data['CHECK_GIDAS'],
                'FIXED_COPAY': data['FIXED_COPAY'],
                'CHECK_DIRECT_FILING': data['CHECK_DIRECT_FILING'],
                'CHECK_PCF_SECONDARY_CR': data['CHECK_PCF_SECONDARY_CR'],
                'CHECK_ASC_SECONDARY_CR': data['CHECK_ASC_SECONDARY_CR'],
                'ACTIVE': data['ACTIVE'],
                'EFF_END_DATE': data['EFF_END_DATE'],
                'CHECK_FACILITY_TSEKAP': data['CHECK_FACILITY_TSEKAP'],
                'CHECK_FACILITY_ABTC': data['CHECK_FACILITY_ABTC'],
                'CHECK_FACILITY_TBDOTSC': data['CHECK_FACILITY_TBDOTSC'],
                'CHECK_FACILITY_OPMC': data['CHECK_FACILITY_OPMC'],
                'CHECK_WHAT_IS_COVERED_BY_AMT': data['CHECK_WHAT_IS_COVERED_BY_AMT'],
                'CHECK_SPC_RELATED_BEN_CODES': 'C19T1 C19T2 C19T3', # temporarily filled with mock data | data['CHECK_SPC_RELATED_BEN_CODES']
                'CHECK_LENGTH_OF_STAY': data['CHECK_LENGTH_OF_STAY'],
                'VALIDATION_RULES': "[[ {'Procedure is performed by an HCP whose PAN begins with any of the following numbers','1304,1501'} = 'true' ,'A86' ]]", # temporarily fill with mock data | data['VALIDATION_RULES']
                'TO_BE_TAGGED_FOR_POST_AUDIT': data['TO_BE_TAGGED_FOR_POST_AUDIT'],
                'CHECK_FACILITY_RHU': data['CHECK_FACILITY_RHU'],
                'CHECK_FACILITY_PCB': data['CHECK_FACILITY_PCB'],
            }
            return self.repository.create(acr_perrvs_rules_data)
        else:
            return None


