import random
from .forms import SAVE_RVS_FORM
from django.shortcuts import render, HttpResponse
from .models import ACR_GROUPS, ACR_GROUPS_ICDS, ACR_GROUPS_RVS, ACR_PERRVS_RULES
from .services import ACR_GROUPS_SERVICE, ACR_GROUPS_RVS_SERVICE, ACR_PERRVS_RULES_SERVICE
from .repositories import ACR_GROUPS_REPOSITORY, ACR_GROUPS_RVS_REPOSITORY, ACR_PERRVS_RULES_REPOSITORY

# Create your views here.
def login(request):
    return render(request, 'pages/login.html')

def groups(request):
    return render(request, 'pages/acr/group-list.html')

def create_rvs(request):

    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
    acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
    acr_perrvs_rules_service = ACR_PERRVS_RULES_SERVICE(ACR_PERRVS_RULES_REPOSITORY())

    if request.method == 'POST':

        print(request.POST) #remove after testing

        form = SAVE_RVS_FORM(request.POST)
        empty_form = SAVE_RVS_FORM()

        try:
            acr_groups = acr_groups_service.create(form)
            acr_groups_rvs = acr_groups_rvs_service.create(form, acr_groups)
            #acr_perrvs_rules = acr_perrvs_rules_service.create(form, acr_groups.ACR_GROUPID, acr_groups_rvs.RVSCODE)

            if acr_groups is not None and acr_groups_rvs is not None:  
                print("ACR_GROUPS created successfully") #remove after testing
                form = SAVE_RVS_FORM()
                return render(request, 'pages/acr/create-rvs.html', {'form': form})
            else:
                print("Form is not valid") #remove after testing
                print(form.errors) #remove after testing
                return render(request, 'pages/acr/create-rvs.html', {'form': form})
        
        except Exception as e:
            
            print(f"An error occurred: {e}") #remove after testing
            return render(request, 'pages/acr/create-rvs.html', {'error_message': str(e)})
    
    form = SAVE_RVS_FORM()
    return render(request, 'pages/acr/create-rvs.html', {'form': form})

def generate_acr_group_id():
    return 'CR' + str(random.randint(1000, 9999))

def create_icds(request):
    return render(request, 'pages/acr/create-icds.html')




