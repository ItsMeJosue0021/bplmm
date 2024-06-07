from django.shortcuts import get_object_or_404 # type: ignore
from django.utils import timezone # type: ignore
from ..models import *

class ACR_GROUPS_RVS_SERVICE:

    def __init__(self, _repository):
        self.repository = _repository   
    
    def create_main(self, data, group_id):     
        return self.repository.create_main(self.to_rvs_array(data, group_id)) 

    def create_temp(self, data, username, temp_acr_groupid = None):
        return self.repository.create_temp(self.to_rvs_array(data, temp_acr_groupid = temp_acr_groupid, username = username)) 
        
    def create_temp_modal(self, data, username, group_id):
        return self.repository.create_temp(self.to_rvs_array(data, group_id = group_id, username = username))   
    
    def create_main_rvs_rules(self, data, group_id, rvs_code):
        main_rule_exists = ACR_PERRVS_RULES.objects.filter(ACR_GROUPID=group_id, RVSCODE=rvs_code, EFF_DATE=getattr(data, 'EFF_DATE')).exists()
        if main_rule_exists:
            raise Exception('A RVS rule with the same effectivity date already exists.')
        return self.repository.create_main_rvs_rules(self.rvs_rules(data, rvs_code = rvs_code, group_id = group_id))
                    
    def create_temp_rvs_rules(self, data, rvs_code, username, group_id = None, temp_acr_groupid = None):
        temp_rule_exists = ACR_PERRVS_RULES_TEMP.objects.filter(TEMP_ACR_GROUPID=temp_acr_groupid, RVSCODE=rvs_code, EFF_DATE=data['EFF_DATE']).exists()
        main_rule_exists = ACR_PERRVS_RULES.objects.filter(ACR_GROUPID=temp_acr_groupid, RVSCODE=rvs_code, EFF_DATE=data['EFF_DATE']).exists()
        if temp_rule_exists or main_rule_exists:
            raise Exception('A RVS rule with the same effectivity date already exists.')
        return self.repository.create_temp_rvs_rules(self.rvs_rules(data, rvs_code = rvs_code, group_id = group_id, temp_acr_groupid = temp_acr_groupid, username = username))

    def update_temp(self, data, rvscode):
        rvs = get_object_or_404(ACR_GROUPS_RVS_TEMP, RVSCODE=rvscode)
        
        self.to_update_rvs_array(rvs, data)
        
        rvs.save()
    
    def update_main(self, data, id):
        pass
    
    def update_main_rvs_rules(self, data, rvscode):
        pass
    
    def update_temp_rvs_rules(self, data, rvscode):
        pass
    
    def to_update_rvs_array(self, rvs, data):
        rvs.RVSCODE = data['RVSCODE'],
        rvs.DESCRIPTION = data['DESCRIPTION'],
        rvs.RVU = data['RVU'],
        rvs.EFF_DATE = data['EFF_DATE'],
        rvs.END_DATE = data['END_DATE']
        
    def to_update_rvs_rules_array(self, rvs_rule, data):
        rvs_rule.RVSCODE = data['RVSCODE'],
        rvs_rule.EFF_DATE = data['EFF_DATE'],
        rvs_rule.PRIMARY_AMOUNT = data['PRIMARY_HOSP_SHARE'] + data['PRIMARY_PROF_SHARE'],
        rvs_rule.PRIMARY_HOSP_SHARE = data['PRIMARY_HOSP_SHARE'],
        rvs_rule.PRIMARY_PROF_SHARE = data['PRIMARY_PROF_SHARE'],
        rvs_rule.SECONDARY_AMOUNT = data['SECONDARY_HOSP_SHARE'] + data['SECONDARY_PROF_SHARE'],
        rvs_rule.SECONDARY_HOSP_SHARE = data['SECONDARY_HOSP_SHARE'],
        rvs_rule.SECONDARY_PROF_SHARE = data['SECONDARY_PROF_SHARE'],
        rvs_rule.PCF_AMOUNT = data['PCF_HOSP_SHARE'] + data['PCF_PROF_SHARE'],
        rvs_rule.PCF_HOSP_SHARE = data['PCF_HOSP_SHARE'],
        rvs_rule.PCF_PROF_SHARE = data['PCF_PROF_SHARE'],
        rvs_rule.CHECK_OCCURS_PER_CLAIM = data['CHECK_OCCURS_PER_CLAIM'],
        rvs_rule.CHECK_OCCURS_PER_PERSON = data['CHECK_OCCURS_PER_PERSON'],
        rvs_rule.CHECK_LATERALITY = data['CHECK_LATERALITY'],
        rvs_rule.CHECK_GENDER = data['CHECK_GENDER'],
        rvs_rule.CHECK_AGE = data['CHECK_AGE'],
        rvs_rule.CHECK_FACILITY_H1 = data['CHECK_FACILITY_H1'],
        rvs_rule.CHECK_FACILITY_H2 = data['CHECK_FACILITY_H2'],
        rvs_rule.CHECK_FACILITY_H3 = data['CHECK_FACILITY_H3'],
        rvs_rule.CHECK_FACILITY_ASC = data['CHECK_FACILITY_ASC'],
        rvs_rule.CHECK_FACILITY_PCF = data['CHECK_FACILITY_PCF'],
        rvs_rule.CHECK_FACILITY_MAT = data['CHECK_FACILITY_MAT'],
        rvs_rule.CHECK_FACILITY_FSDC = data['CHECK_FACILITY_FSDC'],
        rvs_rule.CHECK_SINGLE_PERIOD_DAYS = data['CHECK_SINGLE_PERIOD_DAYS'],
        rvs_rule.CHECK_ADDITIONAL_CODES = data['CHECK_ADDITIONAL_CODES'],
        rvs_rule.CHECK_PREAUTHORIZATION = data['CHECK_PREAUTHORIZATION'],
        rvs_rule.CHECK_QUALIFIER = data['CHECK_QUALIFIER'],
        rvs_rule.DEDUCT_FROM_45DAYS = data['DEDUCT_FROM_45DAYS'],
        rvs_rule.CHECK_GIDAS = data['CHECK_GIDAS'],
        rvs_rule.FIXED_COPAY = data['FIXED_COPAY'],
        rvs_rule.CHECK_DIRECT_FILING = data['CHECK_DIRECT_FILING'],
        rvs_rule.CHECK_PCF_SECONDARY_CR = data['CHECK_PCF_SECONDARY_CR'],
        rvs_rule.CHECK_ASC_SECONDARY_CR = data['CHECK_ASC_SECONDARY_CR'],
        rvs_rule.ACTIVE = data['ACTIVE'],
        rvs_rule.EFF_END_DATE = data['EFF_END_DATE'],
        rvs_rule.CHECK_FACILITY_TSEKAP = data['CHECK_FACILITY_TSEKAP'],
        rvs_rule.CHECK_FACILITY_ABTC = data['CHECK_FACILITY_ABTC'],
        rvs_rule.CHECK_FACILITY_TBDOTSC = data['CHECK_FACILITY_TBDOTSC'],
        rvs_rule.CHECK_FACILITY_OPMC = data['CHECK_FACILITY_OPMC'],
        rvs_rule.CHECK_WHAT_IS_COVERED_BY_AMT = data['CHECK_WHAT_IS_COVERED_BY_AMT'],
        rvs_rule.CHECK_SPC_RELATED_BEN_CODES = data['CHECK_SPC_RELATED_BEN_CODES'],
        rvs_rule.VALIDATION_RULES = data['VALIDATION_RULES'],
        rvs_rule.TO_BE_TAGGED_FOR_POST_AUDIT = data['TO_BE_TAGGED_FOR_POST_AUDIT'],
        rvs_rule.CHECK_FACILITY_RHU = data['CHECK_FACILITY_RHU'],
        rvs_rule.CHECK_FACILITY_PCB = data['CHECK_FACILITY_PCB'], 
    
    def to_rvs_array(self, data, group_id = None, temp_acr_groupid = None, username = None):
        rvs_array = {
            'RVSCODE': data['RVSCODE'] if isinstance(data, dict) else getattr(data, 'RVSCODE'),
            'DESCRIPTION': data.get('DESCRIPTION', data.get('RVS_DESCRIPTION')) if isinstance(data, dict) else getattr(data, 'DESCRIPTION'),
            'RVU': data['RVU'] if isinstance(data, dict) else getattr(data, 'RVU'),
            'EFF_DATE': data.get('EFF_DATE', data.get('RVS_EFF_DATE')) if isinstance(data, dict) else getattr(data, 'EFF_DATE'),
            'END_DATE': data.get('END_DATE', data.get('RVS_END_DATE')) if isinstance(data, dict) else getattr(data, 'END_DATE'),
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        }
        
        if group_id is not None:
            rvs_array['ACR_GROUPID'] = group_id
            
        if temp_acr_groupid is not None:
            rvs_array['TEMP_ACR_GROUPID'] = temp_acr_groupid
            
        if username is not None:
            rvs_array['USERNAME'] = username
            
        return rvs_array     
    
    def rvs_rules(self, data, rvs_code, group_id = None, temp_acr_groupid = None, username = None):
        rules_array = {
            'RVSCODE': rvs_code,
            'EFF_DATE': data['EFF_DATE'] if isinstance(data, dict) else getattr(data, 'EFF_DATE'),
            'PRIMARY_AMOUNT': (data['PRIMARY_HOSP_SHARE'] + data['PRIMARY_PROF_SHARE']) if isinstance(data, dict) else (getattr(data, 'PRIMARY_HOSP_SHARE') + getattr(data, 'PRIMARY_PROF_SHARE')),
            'PRIMARY_HOSP_SHARE': data['PRIMARY_HOSP_SHARE'] if isinstance(data, dict) else getattr(data, 'PRIMARY_HOSP_SHARE'),
            'PRIMARY_PROF_SHARE': data['PRIMARY_PROF_SHARE'] if isinstance(data, dict) else getattr(data, 'PRIMARY_PROF_SHARE'),
            'SECONDARY_AMOUNT': data['SECONDARY_HOSP_SHARE'] + data['SECONDARY_PROF_SHARE'] if isinstance(data, dict) else (getattr(data, 'SECONDARY_HOSP_SHARE') + getattr(data, 'SECONDARY_PROF_SHARE')),
            'SECONDARY_HOSP_SHARE': data['SECONDARY_HOSP_SHARE'] if isinstance(data, dict) else getattr(data, 'SECONDARY_HOSP_SHARE'),
            'SECONDARY_PROF_SHARE': data['SECONDARY_PROF_SHARE'] if isinstance(data, dict) else getattr(data, 'SECONDARY_PROF_SHARE'),
            'PCF_AMOUNT': data['PCF_HOSP_SHARE'] + data['PCF_PROF_SHARE'] if isinstance(data, dict) else (getattr(data, 'PCF_HOSP_SHARE') + getattr(data, 'PCF_PROF_SHARE')),
            'PCF_HOSP_SHARE': data['PCF_HOSP_SHARE'] if isinstance(data, dict) else getattr(data, 'PCF_HOSP_SHARE'),
            'PCF_PROF_SHARE': data['PCF_PROF_SHARE'] if isinstance(data, dict) else getattr(data, 'PCF_PROF_SHARE'),
            'CHECK_OCCURS_PER_CLAIM': data['CHECK_OCCURS_PER_CLAIM'] if isinstance(data, dict) else getattr(data, 'CHECK_OCCURS_PER_CLAIM'),
            'CHECK_OCCURS_PER_PERSON': data['CHECK_OCCURS_PER_PERSON'] if isinstance(data, dict) else getattr(data, 'CHECK_OCCURS_PER_PERSON'),
            'CHECK_LATERALITY': data['CHECK_LATERALITY'] if isinstance(data, dict) else getattr(data, 'CHECK_LATERALITY'),
            'CHECK_GENDER': data['CHECK_GENDER'] if isinstance(data, dict) else getattr(data, 'CHECK_GENDER'),
            'CHECK_AGE': data['CHECK_AGE'] if isinstance(data, dict) else getattr(data, 'CHECK_AGE'),
            'CHECK_FACILITY_H1': data['CHECK_FACILITY_H1'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_H1'), #error here
            'CHECK_FACILITY_H2': data['CHECK_FACILITY_H2'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_H2'),
            'CHECK_FACILITY_H3': data['CHECK_FACILITY_H3'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_H3'),
            'CHECK_FACILITY_ASC': data['CHECK_FACILITY_ASC'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_ASC'),
            'CHECK_FACILITY_PCF': data['CHECK_FACILITY_PCF'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_PCF'),
            'CHECK_FACILITY_MAT': data['CHECK_FACILITY_MAT'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_MAT'),
            'CHECK_FACILITY_FSDC': data['CHECK_FACILITY_FSDC'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_FSDC'),
            'CHECK_SINGLE_PERIOD_DAYS': data['CHECK_SINGLE_PERIOD_DAYS'] if isinstance(data, dict) else getattr(data, 'CHECK_SINGLE_PERIOD_DAYS'),
            'CHECK_ADDITIONAL_CODES': data['CHECK_ADDITIONAL_CODES'] if isinstance(data, dict) else getattr(data, 'CHECK_ADDITIONAL_CODES'),
            'CHECK_PREAUTHORIZATION': data['CHECK_PREAUTHORIZATION'] if isinstance(data, dict) else getattr(data, 'CHECK_PREAUTHORIZATION'),
            'CHECK_QUALIFIER': data['CHECK_QUALIFIER'] if isinstance(data, dict) else getattr(data, 'CHECK_QUALIFIER'),
            'DEDUCT_FROM_45DAYS': data['DEDUCT_FROM_45DAYS'] if isinstance(data, dict) else getattr(data, 'DEDUCT_FROM_45DAYS'),
            'CHECK_GIDAS': data['CHECK_GIDAS'] if isinstance(data, dict) else getattr(data, 'CHECK_GIDAS'),
            'FIXED_COPAY': data['FIXED_COPAY'] if isinstance(data, dict) else getattr(data, 'FIXED_COPAY'),
            'CHECK_DIRECT_FILING': data['CHECK_DIRECT_FILING'] if isinstance(data, dict) else getattr(data, 'CHECK_DIRECT_FILING'),
            'CHECK_PCF_SECONDARY_CR': data['CHECK_PCF_SECONDARY_CR'] if isinstance(data, dict) else getattr(data, 'CHECK_PCF_SECONDARY_CR'),
            'CHECK_ASC_SECONDARY_CR': data['CHECK_ASC_SECONDARY_CR'] if isinstance(data, dict) else getattr(data, 'CHECK_ASC_SECONDARY_CR'),
            'ACTIVE': data['ACTIVE'] if isinstance(data, dict) else getattr(data, 'ACTIVE'),
            'EFF_END_DATE': data['EFF_END_DATE'] if isinstance(data, dict) else getattr(data, 'EFF_END_DATE'),
            'CHECK_FACILITY_TSEKAP': data['CHECK_FACILITY_TSEKAP'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_TSEKAP'),
            'CHECK_FACILITY_ABTC': data['CHECK_FACILITY_ABTC'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_ABTC'),
            'CHECK_FACILITY_TBDOTSC': data['CHECK_FACILITY_TBDOTSC'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_TBDOTSC'),
            'CHECK_FACILITY_OPMC': data['CHECK_FACILITY_OPMC'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_OPMC'),
            'CHECK_WHAT_IS_COVERED_BY_AMT': data['CHECK_WHAT_IS_COVERED_BY_AMT'] if isinstance(data, dict) else getattr(data, 'CHECK_WHAT_IS_COVERED_BY_AMT'),
            'CHECK_SPC_RELATED_BEN_CODES': data['CHECK_SPC_RELATED_BEN_CODES'] if isinstance(data, dict) else getattr(data, 'CHECK_SPC_RELATED_BEN_CODES'),
            'CHECK_LENGTH_OF_STAY': data['CHECK_LENGTH_OF_STAY'] if isinstance(data, dict) else getattr(data, 'CHECK_LENGTH_OF_STAY'),
            'VALIDATION_RULES': data['VALIDATION_RULES'] if isinstance(data, dict) else getattr(data, 'VALIDATION_RULES'),
            'TO_BE_TAGGED_FOR_POST_AUDIT': data['TO_BE_TAGGED_FOR_POST_AUDIT'] if isinstance(data, dict) else getattr(data, 'TO_BE_TAGGED_FOR_POST_AUDIT'),
            'CHECK_FACILITY_RHU': data['CHECK_FACILITY_RHU'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_RHU'),
            'CHECK_FACILITY_PCB': data['CHECK_FACILITY_PCB'] if isinstance(data, dict) else getattr(data, 'CHECK_FACILITY_PCB'),
        }
        
        if group_id is not None:
            rules_array['ACR_GROUPID'] = group_id
            
        if temp_acr_groupid is not None:
            rules_array['TEMP_ACR_GROUPID'] = temp_acr_groupid
        
        if username is not None:
            rules_array['USERNAME'] = username
        return rules_array
        
        
        