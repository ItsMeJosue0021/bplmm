# Group Service Layer
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