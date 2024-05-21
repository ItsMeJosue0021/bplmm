from django import forms # type: ignore
from .models import ACR_GROUPS, ACR_GROUPS_ICDS, ACR_GROUPS_RVS, ACR_PERRVS_RULES

class ACR_GROUPS_FORM(forms.Form):
    DESCRIPTION = forms.CharField(widget=forms.Textarea)
    EFF_DATE = forms.DateField()
    END_DATE = forms.DateField()

class SAVE_RVS_FORM(forms.Form):
    DESCRIPTION = forms.CharField(widget=forms.Textarea)
    RVSCODE = forms.CharField(max_length=255)
    RVU = forms.IntegerField()
    EFF_DATE = forms.DateField()
    END_DATE = forms.DateField()

class SAVE_GROUP_RVS_RULES(forms.Form):
    
    GROUP_DESCRIPTION = forms.CharField(widget=forms.Textarea)
    GROUP_EFF_DATE = forms.DateField()
    GROUP_END_DATE = forms.DateField()
    
    RVS_DESCRIPTION = forms.CharField(widget=forms.Textarea)
    RVSCODE = forms.CharField(max_length=255)
    RVU = forms.IntegerField()
    RVS_EFF_DATE = forms.DateField()
    RVS_END_DATE = forms.DateField()
    
    EFF_DATE = forms.DateField()
    EFF_END_DATE = forms.DateField()
    PRIMARY_HOSP_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    PRIMARY_PROF_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    SECONDARY_HOSP_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    SECONDARY_PROF_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    PCF_HOSP_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    PCF_PROF_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)

    FIXED_COPAY = forms.DecimalField(max_digits=10, decimal_places=2)
    CHECK_OCCURS_PER_CLAIM = forms.CharField(max_length=255)
    CHECK_SINGLE_PERIOD_DAYS = forms.CharField(max_length=255)
    CHECK_OCCURS_PER_PERSON = forms.CharField(max_length=255)
    CHECK_AGE = forms.CharField(max_length=255)
    CHECK_LENGTH_OF_STAY = forms.CharField(max_length=255)
    CHECK_GENDER = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])

    ACTIVE = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H1 = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H2 = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H3 = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_ASC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_PCF = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_MAT = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_FSDC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_DIRECT_FILING = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_GIDAS = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])

    CHECK_PCF_SECONDARY_CR = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_ASC_SECONDARY_CR = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_PREAUTHORIZATION = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_LATERALITY = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_OPMC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TBDOTSC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TSEKAP = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_ABTC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])

    TO_BE_TAGGED_FOR_POST_AUDIT = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_RHU = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_PCB = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_QUALIFIER = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_WHAT_IS_COVERED_BY_AMT = forms.CharField(max_length=255)

    CHECK_ADDITIONAL_CODES = forms.CharField(widget=forms.Textarea)
    CHECK_SPC_RELATED_BEN_CODES = forms.CharField(widget=forms.Textarea)
    DEDUCT_FROM_45DAYS = forms.CharField(max_length=255)
    VALIDATION_RULES = forms.CharField(widget=forms.Textarea)
    
    OPERATOR = forms.CharField(max_length=255)
    MINIMUM = forms.CharField(max_length=255)
    MINIMUM_YD = forms.CharField(max_length=255)
    MAXIMUM = forms.CharField(max_length=255)
    MAXIMUM_YD = forms.CharField(max_length=255)
    
    CONDITIONAL = forms.CharField(max_length=255)
    DEDUCT_FROM_45DAYS_TYPE = forms.CharField(max_length=255)
    DEDUCT_FROM_45DAYS_NUMBER = forms.CharField(max_length=255)
    DEDUCT_FROM_45DAYS_DAYS = forms.CharField(max_length=255)
    
class SAVE_RVS_RULES(forms.Form):
    EFF_DATE = forms.DateField()
    EFF_END_DATE = forms.DateField()
    PRIMARY_HOSP_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    PRIMARY_PROF_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    SECONDARY_HOSP_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    SECONDARY_PROF_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    PCF_HOSP_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)
    PCF_PROF_SHARE = forms.DecimalField(max_digits=10, decimal_places=2)

    FIXED_COPAY = forms.DecimalField(max_digits=10, decimal_places=2)
    CHECK_OCCURS_PER_CLAIM = forms.CharField(max_length=255)
    CHECK_SINGLE_PERIOD_DAYS = forms.CharField(max_length=255)
    CHECK_OCCURS_PER_PERSON = forms.CharField(max_length=255)
    CHECK_AGE = forms.CharField(max_length=255)
    CHECK_GENDER = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])

    ACTIVE = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H1 = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H2 = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H3 = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_ASC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_PCF = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_MAT = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_FSDC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_DIRECT_FILING = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_GIDAS = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])

    CHECK_PCF_SECONDARY_CR = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_ASC_SECONDARY_CR = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False')])
    CHECK_PREAUTHORIZATION = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_LATERALITY = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_OPMC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TBDOTSC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TSEKAP = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_ABTC = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])

    TO_BE_TAGGED_FOR_POST_AUDIT = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_RHU = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_PCB = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_QUALIFIER = forms.ChoiceField(choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_WHAT_IS_COVERED_BY_AMT = forms.CharField(max_length=255)
    CHECK_LENGTH_OF_STAY = forms.CharField(max_length=255)

    CHECK_ADDITIONAL_CODES = forms.CharField(widget=forms.Textarea)
    CHECK_SPC_RELATED_BEN_CODES = forms.CharField(widget=forms.Textarea)
    DEDUCT_FROM_45DAYS = forms.CharField(max_length=255)
    VALIDATION_RULES = forms.CharField(widget=forms.Textarea)
    

