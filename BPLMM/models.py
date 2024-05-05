from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore

# Create your models here.

class CustomUser(AbstractUser):
    is_encoder = models.BooleanField(default=False)
    is_approver = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

class ACR_GROUPS(models.Model):
    ACR_GROUPID = models.CharField(max_length=255, primary_key=True)
    DESCRIPTION = models.TextField()
    EFF_DATE = models.DateField()
    ACTIVE = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    END_DATE = models.DateField(null=True, blank=True)

class ACR_GROUPS_TEMP(models.Model):
    ID = models.AutoField(primary_key=True)
    ACR_GROUPID = models.CharField(max_length=255, null=True, default='N/A')
    DESCRIPTION = models.TextField()
    EFF_DATE = models.DateField()
    ACTIVE = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    END_DATE = models.DateField(null=True, blank=True)
    USERNAME = models.CharField(max_length=255)

class ACR_GROUPS_LOG(models.Model):
    ACR_GROUPID = models.CharField(max_length=255)
    LOG_DATE_TIME = models.DateTimeField(auto_now_add=True)
    REMARKS = models.TextField()
    USERNAME = models.CharField(max_length=255)
    UPDATED_CULOMNS = models.TextField()
    PREVIOUS_COLUMN_VALUE = models.TextField()

class ACR_GROUPS_ICDS(models.Model):
    ICDCODE = models.CharField(max_length=255, primary_key=True)
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    DESCRIPTION = models.TextField()
    EFF_DATE = models.DateField()

class ACR_GROUPS_ICDS_TEMP(models.Model):
    ID = models.AutoField(primary_key=True)
    ICDCODE = models.CharField(max_length=255, null=True, default='N/A')
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    DESCRIPTION = models.TextField()
    EFF_DATE = models.DateField()
    USERNAME = models.CharField(max_length=255)

class ACR_GROUPS_ICDS_LOG(models.Model):
    ICDCODE = models.CharField(max_length=255)
    LOG_DATE_TIME = models.DateTimeField(auto_now_add=True)
    REMARKS = models.TextField()
    USERNAME = models.CharField(max_length=255)
    UPDATED_CULOMNS = models.TextField()
    PREVIOUS_COLUMN_VALUE = models.TextField()

class ACR_GROUPS_RVS(models.Model):
    RVSCODE = models.CharField(max_length=255, primary_key=True)
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    DESCRIPTION = models.TextField()
    RVU = models.IntegerField()
    EFF_DATE = models.DateField()
    END_DATE = models.DateField(null=True, blank=True)

class ACR_GROUPS_RVS_TEMP(models.Model):
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    DESCRIPTION = models.TextField()
    RVU = models.IntegerField()
    EFF_DATE = models.DateField()
    END_DATE = models.DateField(null=True, blank=True)
    USERNAME = models.CharField(max_length=255)

class ACR_GROUPS_RVS_LOG(models.Model):
    RVSCODE = models.CharField(max_length=255)
    LOG_DATE_TIME = models.DateTimeField(auto_now_add=True)
    REMARKS = models.TextField()
    USERNAME = models.CharField(max_length=255)
    UPDATED_CULOMNS = models.TextField()
    PREVIOUS_COLUMN_VALUE = models.TextField()

class ACR_PERRVS_RULES(models.Model):
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    RVSCODE = models.CharField(max_length=255) 
    EFF_DATE = models.DateField()
    PRIMARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2) 
    SECONDARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    CHECK_OCCURS_PER_CLAIM = models.CharField(max_length=255)
    CHECK_OCCURS_PER_PERSON = models.CharField(max_length=255)  
    CHECK_LATERALITY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_GENDER = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])
    CHECK_AGE = models.CharField(max_length=255)  
    CHECK_FACILITY_H1 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H2 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H3 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_ASC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_PCF = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_MAT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_FSDC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_SINGLE_PERIOD_DAYS = models.CharField(max_length=255)  
    CHECK_ADDITIONAL_CODES = models.TextField()
    CHECK_PREAUTHORIZATION = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_QUALIFIER = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    DEDUCT_FROM_45DAYS = models.CharField(max_length=255)  
    CHECK_GIDAS = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    FIXED_COPAY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_DIRECT_FILING = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_PCF_SECONDARY_CR =models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_ASC_SECONDARY_CR = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    ACTIVE = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    EFF_END_DATE = models.DateField()
    CHECK_FACILITY_TSEKAP = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_ABTC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TBDOTSC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_OPMC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_WHAT_IS_COVERED_BY_AMT = models.CharField(max_length=255)
    CHECK_SPC_RELATED_BEN_CODES = models.TextField()
    CHECK_LENGTH_OF_STAY = models.CharField(max_length=255) 
    VALIDATION_RULES = models.TextField()
    TO_BE_TAGGED_FOR_POST_AUDIT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_RHU = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_PCB = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])

class ACR_PERRVS_RULES_TEMP(models.Model):
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    RVSCODE = models.CharField(max_length=255) 
    EFF_DATE = models.DateField()
    PRIMARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2) 
    SECONDARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    CHECK_OCCURS_PER_CLAIM = models.CharField(max_length=255)
    CHECK_OCCURS_PER_PERSON = models.CharField(max_length=255)  
    CHECK_LATERALITY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_GENDER = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])
    CHECK_AGE = models.CharField(max_length=255)  
    CHECK_FACILITY_H1 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H2 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H3 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_ASC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_PCF = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_MAT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_FSDC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_SINGLE_PERIOD_DAYS = models.CharField(max_length=255)  
    CHECK_ADDITIONAL_CODES = models.TextField()
    CHECK_PREAUTHORIZATION = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_QUALIFIER = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    DEDUCT_FROM_45DAYS = models.CharField(max_length=255)  
    CHECK_GIDAS = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    FIXED_COPAY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_DIRECT_FILING = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_PCF_SECONDARY_CR =models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_ASC_SECONDARY_CR = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    ACTIVE = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    EFF_END_DATE = models.DateField()
    CHECK_FACILITY_TSEKAP = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_ABTC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TBDOTSC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_OPMC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_WHAT_IS_COVERED_BY_AMT = models.CharField(max_length=255)
    CHECK_SPC_RELATED_BEN_CODES = models.TextField()
    CHECK_LENGTH_OF_STAY = models.CharField(max_length=255) 
    VALIDATION_RULES = models.TextField()
    TO_BE_TAGGED_FOR_POST_AUDIT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_RHU = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_PCB = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    USERNAME = models.CharField(max_length=255)

class ACR_PERRVS_RULES_LOG(models.Model):
    RVSCODE = models.CharField(max_length=255)
    LOG_DATE_TIME = models.DateTimeField(auto_now_add=True)
    REMARKS = models.TextField()
    USERNAME = models.CharField(max_length=255)
    UPDATED_CULOMNS = models.TextField()
    PREVIOUS_COLUMN_VALUE = models.TextField()

class ACR_PERICD_RULES(models.Model):
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    ICDCODE = models.CharField(max_length=255) 
    EFF_DATE = models.DateField()
    PRIMARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2) 
    SECONDARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    CHECK_OCCURS_PER_CLAIM = models.CharField(max_length=255)
    CHECK_OCCURS_PER_PERSON = models.CharField(max_length=255)  
    HECK_LATERALITY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_GENDER = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])
    CHECK_AGE = models.CharField(max_length=255)  
    CHECK_FACILITY_H1 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H2 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H3 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_ASC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_PCF = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_MAT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_FSDC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_SINGLE_PERIOD_DAYS = models.CharField(max_length=255)  
    CHECK_ADDITIONAL_CODES = models.TextField()
    CHECK_PREAUTHORIZATION = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_QUALIFIER = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    DEDUCT_FROM_45DAYS = models.CharField(max_length=255)  
    CHECK_GIDAS = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    FIXED_COPAY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_DIRECT_FILING = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_PCF_SECONDARY_CR =models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_ASC_SECONDARY_CR = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    ACTIVE = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    EFF_END_DATE = models.DateField()
    CHECK_FACILITY_TSEKAP = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_ABTC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TBDOTSC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_OPMC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_SPC_RELATED_BEN_CODES = models.TextField()
    CHECK_LENGTH_OF_STAY = models.CharField(max_length=255) 
    VALIDATION_RULES = models.TextField()
    TO_BE_TAGGED_FOR_POST_AUDIT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_RHU = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_PCB = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])

class ACR_PERICD_RULES_TEMP(models.Model):
    ACR_GROUPID = models.ForeignKey(ACR_GROUPS, on_delete=models.CASCADE)
    ICDCODE = models.CharField(max_length=255) 
    EFF_DATE = models.DateField()
    PRIMARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PRIMARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2) 
    SECONDARY_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    SECONDARY_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_AMOUNT = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_HOSP_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    PCF_PROF_SHARE = models.DecimalField(max_digits=10, decimal_places=2)  
    CHECK_OCCURS_PER_CLAIM = models.CharField(max_length=255)
    CHECK_OCCURS_PER_PERSON = models.CharField(max_length=255)  
    HECK_LATERALITY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_GENDER = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('B', 'Both')])
    CHECK_AGE = models.CharField(max_length=255)  
    CHECK_FACILITY_H1 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H2 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_H3 = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_ASC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_PCF = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_MAT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_FACILITY_FSDC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_SINGLE_PERIOD_DAYS = models.CharField(max_length=255)  
    CHECK_ADDITIONAL_CODES = models.TextField()
    CHECK_PREAUTHORIZATION = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_QUALIFIER = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    DEDUCT_FROM_45DAYS = models.CharField(max_length=255)  
    CHECK_GIDAS = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    FIXED_COPAY = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_DIRECT_FILING = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_PCF_SECONDARY_CR =models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    CHECK_ASC_SECONDARY_CR = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    ACTIVE = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False')])
    EFF_END_DATE = models.DateField()
    CHECK_FACILITY_TSEKAP = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_ABTC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_TBDOTSC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_OPMC = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_SPC_RELATED_BEN_CODES = models.TextField()
    CHECK_LENGTH_OF_STAY = models.CharField(max_length=255) 
    VALIDATION_RULES = models.TextField()
    TO_BE_TAGGED_FOR_POST_AUDIT = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_RHU = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    CHECK_FACILITY_PCB = models.CharField(max_length=3, choices=[('T', 'True'), ('F', 'False'), ('N/A', 'Not Applicable')])
    USERNAME = models.CharField(max_length=255)

class ACR_PERICD_RULES_LOG(models.Model):
    ICDCODE = models.CharField(max_length=255)
    LOG_DATE_TIME = models.DateTimeField(auto_now_add=True)
    REMARKS = models.TextField()
    USERNAME = models.CharField(max_length=255)
    UPDATED_CULOMNS = models.TextField()
    PREVIOUS_COLUMN_VALUE = models.TextField()


