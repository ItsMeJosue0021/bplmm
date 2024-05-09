from django.core.management.base import BaseCommand # type: ignore
from BPLMM.models import CLAIM_VALIDATION_INFOS

class Command(BaseCommand):
    help = 'Seed CLAIM VALIDATION INFOS'

    def handle(self, *args, **kwargs):
        contents = [
            'Length of stay in hours', 
            'Patient age', 
            'Discharge disposition', 
            'Count of the following procedures performed by attending HCP within the same day of the procedure of this claim', 
            'Count of the following procedures performed by attending HCP within the month of the procedure of this claim',
            'Date of the latest among the following procedures that are done before this claim (with the same laterality)', 
            'Has valid 2PR or 2CC override code', 
            'Is exempted from CPSA rules', 
            'Is traumatic or glaucomatous cataract included in diagnosis', 
            'Is childhood cataract included in the diagnosis',
            'Is exempted from cataract procedure count limit per HCP', 
            'Patient sex', 
            'Patient age in days', 
            'Patient age in months', 
            'Admission date',
            'First Case Rate belongs to any of the following ACR Group ID', 
            'First Case Rate ICD Code is in list', 
            'HCP class is', 
            'HCP has training code', 
            'Count of the following procedures performed within the month of the procedure of this claim by attending HCP with the specified PAN prefixes', 
            'Count of the following procedures performed within the same day of the procedure of this claim by attending HCP with the specified PAN prefixes', 
            'Was HCP allowed to perform IUD insertion before 10/03/2015', 
            'Has attached checklist of mandatory and other services', 
            'Has attached detoxification treatment plan',
            'Has attached photocopy of completely accomplished satisfaction questionnaire', 
            'Has attached checklist of requirement for reimbursement', 
            'Has attached checklist of co-morbidity form', 
            'ICD code of first case rate', 
            'RVS code of first case rate',
            'HCI has any of the following service codes', 
            'HCI classification', 
            'Count of good claims of the patient for the same procedure within the quarter', 
            'Laboratory number is not yet used by other patients', 
            'Laboratory number is same with that of previous claims',
            'Count of good claims of the patient for the same procedure within the year', 
            'Laboratory number', 
            'Is treatment/procedure done abroad', 
            'Has no similar good procedure claim within the indicated period', 
            'Was HCP allowed to perform IUD insertion', 
            'HCI class', 
            'Was attended by a doctor', 
            'date of procedure', 
            'number of similar procedures performed by attending HCP within the same day as this procedure',
            'number of similar procedures performed by attending HCP within the month as this procedure', 
            'Procedure is performed by an HCP whose PAN begins with any of the following numbers', 
            'Patient received any of the following procedures within indicated days', 
            'laterality of procedure', 
            'Any of the following ICD codes is present in discharged diagnosis',
            'Has date of procedure', 
            'Has CPSA', 
            'CPSA Number is valid', 
            'IOL is not expired prior to the procedure', 
            'Patient received any of the following procedures regardless of the status of claim',
            'IOL serial number is already used', 
            'Number of claims with the specified ICD code in the diagnosis', 
            'Has IOL sticker', 
            'CPSA Number is already used', 
            'Date of the latest among the following procedures that are done before this claim', 
            'Patient received any of the following procedures before this claim', 
            'Initial tranche has been paid', 
            'Claim is filed beyond 60 calendar days after the date of measurement', 
            'Has a valid value for date of fitting of the device', 
            'Claim is filed beyond 60 calendar days after the fitting of the device', 
            'Claim for an expected tranche of this Z-benefit package exists', 
            'Patient birthdate',
            'Add months', 
            'With attached valid Case Investigation Form (CIF)', 
            'With attached valid SARS-COV-2 Claim Summary Form (SCSF)', 
            'Discharge date', 
            'HCI PMCC Number',
            'The patient is the member', 
            'Field for patient priority subgroup has value', 
            'Attending eye specialist has not reached the 10 cataract operations per day', 
            'Attending eye specialist has not reached the 50 cataract operations per month', 
            'Field for services covered has value',
            'Flag for donated test kits has value', 
            'Has override code', 
            'Months from the birthdate of patient', 
            'Months from the birthdate of the patient', 
            'Patient age matches with patient priority subgroup', 
            'Has PDD Registry Number', 
            'HF is located in GIDA', 
            'With attached neuroimaging result (NIR)',
            'With attached radiographic result (RGR)', 
            'With breast cancer treatment passport', 
            'With photocopy of the multidisciplinary team (MDT) plan', 
            'With original or CTC of the Statement of Account (SOA) or its equivalent', 
            'Claim is refiled',
            'Claim is filed within the allowable 30 calendar day period following the completion of the rendered service', 
            'Attending eye specialist has not reached the 200 cataract operations per month', 
            'Is transferred to Level 2 or Level 3 hospital', 
            'Is transfer of CHIBP patient to the target HCI allowed', 
            'Patient has previously availed of the Z Benefits for assistive device, training and rehabilitation service', 
            'Rehab therapy with inputs of date and number of sessions received', 
            'Has valid patient priority subgroup for 2022-Aug-31 and onwards', 
            'Has valid patient priority subgroup for 31-Aug-2022 and onwards',
            'Has received the miniumun number of rehabilitation sessions', 
            'Has CF1 or PBEF', 
            'Procedure date of this claim coincides with the admission date of its related claim', 
            'Patient priority subgroup', 
            'Package has not yet been availed in the corresponding admission',
            'With valid Membership Empowerment Form (MEF)', 
            'With valid PhilHealth Claim Form 2 (CF2)', 
            'With photocopy of certificate of completed training on the safe and functional use of devices', 
            'Count of filed claims of the patient for the specified benefit package codes', 
            'Is claimed as first case rate',
            'Is claimed as second case rate', 
            'Has second case rate amount', 
            'Has first case rate amount', 
            'Claim validation status of first case rate', 
            'Patient is a health worker', 
            'With attached valid employment/deployment certificate of the Patient - Health Worker', 
            'Claim is directly filed', 
            'With attached valid itemized billing',
            'Count of filed claims of the patient for the specified benefit package codes within the year', 
            'Count of filed claims of the patient for the specified Z-benefit package codes within the year', 
            'With attached photocopy of Certificate of Assessment and recommendations from medical specialist', 
            'Has rehabilitation therapy with inputs of date and number of session received', 
            'Has photocopy of certificate of completed training on the safe and functional use of devices',
            'Has photocopy of certificate of outcomes after rehabilitation sessions', 
            'Age of availment is between', 
            'Age of availment must be', 
            'Claim for an expected tranche of this Z-benefit package is not found', 
            'Claim for an expected tranche of this Z-benefit package is found',
            'Procedure/service provided by a medical oncologist', 
            'Patient passed all eligibilty criteria', 
            'With transmittal form', 
            'With certificate of hearing aid verification', 
            'With certificate of completed speech therapy sessions', 
            'With photocopy of ABR waveform tracing or applicable hearing test result', 
            'With photocopy of hearing test result', 
            'With photocopy of hispathology report',
            'With photocopy of accomplished surgical operative report', 
            'With photocopy of accomplished anesthesia report', 
            'Complete services have been rendered', 
            'With donated test kits', 
            'Is referred from a hospital',
            'Has valid patient priority subgroup', 
            'Complete services have been rendered for C19T1 claims', 
            'Complete services have been rendered for C19T2 claims',
            'Complete services have been rendered for C19T3 claims', 
            'Has valid value for the date of completion of assessment', 
            'Date of submission of claim is not later than 30 days after the date of completion of assessment', 
            'Has valid value for the last date of therapy session for the specific tranche', 
            'Date of submission of claim is not later than 30 days after the last date of therapy session for the specified tranche',
            'Has a valid value for the date of measurement'
         ]
        
        for content in contents:
            CLAIM_VALIDATION_INFOS.objects.create(CONTENT=content)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    