from django.utils import timezone # type: ignore
from ..models import *

class ACR_GROUPS_RVS_SERVICE:

    def __init__(self, _repository):
        self.repository = _repository        

    def create_temp(self, data, group_id, request):
        return self.repository.create_temp(self.to_rvs_array(data, group_id, request)) 
        
    def create_temp_modal(self, data, group_id, request):
        return self.repository.create_temp(self.to_rvs_array(data, group_id, request))   
    
    def create_main_rvs_rules(self, data, group_id, rvs_code):
        return self.repository.create_main_rvs_rules(self.to_rules_array(data, group_id, rvs_code))
                    
    def create_temp_rvs_rules(self, data, group_id, rvs_code, username):
        temp_rule_exists = ACR_PERRVS_RULES_TEMP.objects.filter(ACR_GROUPID=group_id, RVSCODE=rvs_code, EFF_DATE=data['EFF_DATE']).exists()
        main_rule_exists = ACR_PERRVS_RULES.objects.filter(ACR_GROUPID=group_id, RVSCODE=rvs_code, EFF_DATE=data['EFF_DATE']).exists()
        if temp_rule_exists or main_rule_exists:
            raise Exception('A rule with the same effectivity date already exists.')
        return self.repository.create_temp_rvs_rules(self.to_rules_array(data, group_id, rvs_code, username))

    def to_rvs_array(self, data, group_id, request):
        rvs_array = {
            'RVSCODE': data['RVSCODE'],
            'ACR_GROUPID': group_id,
            'DESCRIPTION': data.get('DESCRIPTION', data.get('RVS_DESCRIPTION')),
            'RVU': data['RVU'],
            'EFF_DATE': data.get('EFF_DATE', data.get('RVS_EFF_DATE')),
            'END_DATE': data.get('END_DATE', data.get('RVS_END_DATE')),
            'USERNAME': request.user.username,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        }
        return rvs_array  
    
    def to_rules_array(self, data, group_id, rvs_code, username = None):
        rules_array = {
            'ACR_GROUPID': group_id,
            'RVSCODE': rvs_code,
            'EFF_DATE': data['EFF_DATE'],
            'PRIMARY_AMOUNT': data['PRIMARY_HOSP_SHARE'] + data['PRIMARY_PROF_SHARE'],
            'PRIMARY_HOSP_SHARE': data['PRIMARY_HOSP_SHARE'],
            'PRIMARY_PROF_SHARE': data['PRIMARY_PROF_SHARE'],
            'SECONDARY_AMOUNT': data['SECONDARY_HOSP_SHARE'] + data['SECONDARY_PROF_SHARE'],
            'SECONDARY_HOSP_SHARE': data['SECONDARY_HOSP_SHARE'],
            'SECONDARY_PROF_SHARE': data['SECONDARY_PROF_SHARE'],
            'PCF_AMOUNT': data['PCF_HOSP_SHARE'] + data['PCF_PROF_SHARE'],
            'PCF_HOSP_SHARE': data['PCF_HOSP_SHARE'],
            'PCF_PROF_SHARE': data['PCF_PROF_SHARE'],
            'CHECK_OCCURS_PER_CLAIM': data['CHECK_OCCURS_PER_CLAIM'],
            'CHECK_OCCURS_PER_PERSON': data['CHECK_OCCURS_PER_PERSON'],
            'CHECK_LATERALITY': data['CHECK_LATERALITY'],
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
            'CHECK_ADDITIONAL_CODES': data['CHECK_ADDITIONAL_CODES'], 
            'CHECK_PREAUTHORIZATION': data['CHECK_PREAUTHORIZATION'],
            'CHECK_QUALIFIER': data['CHECK_QUALIFIER'],
            'DEDUCT_FROM_45DAYS': data['DEDUCT_FROM_45DAYS'], 
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
            'CHECK_SPC_RELATED_BEN_CODES': data['CHECK_SPC_RELATED_BEN_CODES'], 
            'CHECK_LENGTH_OF_STAY': data['CHECK_LENGTH_OF_STAY'],
            'VALIDATION_RULES': data['VALIDATION_RULES'],
            'TO_BE_TAGGED_FOR_POST_AUDIT': data['TO_BE_TAGGED_FOR_POST_AUDIT'],
            'CHECK_FACILITY_RHU': data['CHECK_FACILITY_RHU'],
            'CHECK_FACILITY_PCB': data['CHECK_FACILITY_PCB'],
        }
        
        if username is not None:
            rules_array['USERNAME'] = username
        return rules_array
        
        
        