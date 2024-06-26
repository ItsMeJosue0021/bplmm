import random

class ACR_GROUPS_SERVICE:

    def __init__(self, _repository):
        self.repository = _repository

    # Add a new object to the TEMPORARY ACR GROUPS table
    def create_temp(self, form, request):    
        data = form.cleaned_data
        acr_temp_group_data = {
            'DESCRIPTION': data['DESCRIPTION'],
            'EFF_DATE': data['EFF_DATE'],
            'ACTIVE': 'F',
            'END_DATE': data['END_DATE'],
            'USERNAME': request.user.username
        }
        return self.repository.create_temp(acr_temp_group_data)
    
    # Add new object to the MAIN ACR GROUPS table
    def create_main(self, acr_group_data):

        acr_group_data = {
            'ACR_GROUPID': self.generate_acr_group_id(),
            'DESCRIPTION': acr_group_data.DESCRIPTION,
            'EFF_DATE': acr_group_data.EFF_DATE,
            'ACTIVE': 'T',
            'END_DATE': acr_group_data.END_DATE
        }
        return self.repository.create_main(acr_group_data)
    
    # Generates a mock ACR_GROUPID by getting the most recent ACR_GROUPID and incrementing it
    def generate_acr_group_id(self):
        group_id = self.repository.get_most_recent_groupid()
        if group_id:
            prefix = group_id[:2]  
            number = int(group_id[2:])  
            number += 1 
            new_group_id = prefix + str(number) 
            return new_group_id
        else:
            return 'CR1000'
    




  
        
class ACR_PERRVS_RULES_SERVICE:

    def __init__(self, _repository):
        self.repository = _repository

    def create_main(self, data, group_id, rvs_code):
        return self.repository.create_main(self.to_rules_array(data, group_id, rvs_code))
        
    def create_temp(self, data, group_id, rvs_code):
            return self.repository.create_temp(self.to_rules_array(data, group_id, rvs_code))
        
        
    def update(self, form, acr_groupid, rvscodes):
        pass
        
    def to_rules_array(self, data, group_id, rvs_code):
        return {
            'ACR_GROUPID': group_id,
            'RVSCODE': rvs_code,
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
            'CHECK_AGE': data['CHECK_AGE'],
            'CHECK_FACILITY_H1': data['CHECK_FACILITY_H1'],
            'CHECK_FACILITY_H2': data['CHECK_FACILITY_H2'],
            'CHECK_FACILITY_H3': data['CHECK_FACILITY_H3'],
            'CHECK_FACILITY_ASC': data['CHECK_FACILITY_ASC'],
            'CHECK_FACILITY_PCF': data['CHECK_FACILITY_PCF'],
            'CHECK_FACILITY_MAT': data['CHECK_FACILITY_MAT'],
            'CHECK_FACILITY_FSDC': data['CHECK_FACILITY_FSDC'],
            'CHECK_SINGLE_PERIOD_DAYS': data['CHECK_SINGLE_PERIOD_DAYS'],
            'CHECK_ADDITIONAL_CODES': data['CHECK_ADDITIONAL_CODES'], # temporarily filled with mock data | data['CHECK_ADDITIONAL_CODES']
            'CHECK_PREAUTHORIZATION': data['CHECK_PREAUTHORIZATION'],
            'CHECK_QUALIFIER': data['CHECK_QUALIFIER'],
            'DEDUCT_FROM_45DAYS': data['DEDUCT_FROM_45DAYS'], # temporarily filled with mock data | data['DEDUCT_FROM_45DAYS']
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
            'CHECK_SPC_RELATED_BEN_CODES': data['CHECK_SPC_RELATED_BEN_CODES'], # temporarily filled with mock data | data['CHECK_SPC_RELATED_BEN_CODES']
            'CHECK_LENGTH_OF_STAY': data['CHECK_LENGTH_OF_STAY'],
            'VALIDATION_RULES': data['VALIDATION_RULES'], # temporarily fill with mock data | data['VALIDATION_RULES'] | "[[ {'Procedure is performed by an HCP whose PAN begins with any of the following numbers','1304,1501'} = 'true' ,'A86' ]]"
            'TO_BE_TAGGED_FOR_POST_AUDIT': data['TO_BE_TAGGED_FOR_POST_AUDIT'],
            'CHECK_FACILITY_RHU': data['CHECK_FACILITY_RHU'],
            'CHECK_FACILITY_PCB': data['CHECK_FACILITY_PCB']
        }
        


