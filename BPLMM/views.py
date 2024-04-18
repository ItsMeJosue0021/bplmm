import random
from .forms import SAVE_RVS_FORM
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import encoder_required, approver_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .services import ACR_GROUPS_SERVICE, ACR_GROUPS_RVS_SERVICE, ACR_PERRVS_RULES_SERVICE
from .repositories import ACR_GROUPS_REPOSITORY, ACR_GROUPS_RVS_REPOSITORY, ACR_PERRVS_RULES_REPOSITORY


# Create your views here.

def login(request):
    if request.method == 'POST':
        print(request.POST) #remove after testing
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('nag login')
            auth_login(request, user)
            if user.groups.filter(name='Encoder').exists():
                return redirect('create_rvs')
            elif user.groups.filter(name='Approver').exists():
                return redirect('create_icds')
            else:
                auth_logout(request)
                print('nag logout')
                return redirect('login')  
        else:
            print('hindi nag login')
            return render(request, 'pages/login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'pages/login.html')
    

def logout(request):
    auth_logout(request)
    print('nag logout')
    return redirect('login')



@login_required
def groups(request):
    return render(request, 'pages/acr/encoder/group-list.html')

@encoder_required
@login_required
def create_rvs(request):

    acr_groups_service = ACR_GROUPS_SERVICE(ACR_GROUPS_REPOSITORY())
    acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())
    acr_perrvs_rules_service = ACR_PERRVS_RULES_SERVICE(ACR_PERRVS_RULES_REPOSITORY())

    if request.method == 'POST':

        print(request.POST) #remove after testing

        form = SAVE_RVS_FORM(request.POST)

        try:
            acr_groups = acr_groups_service.create(form)
            acr_groups_rvs = acr_groups_rvs_service.create(form, acr_groups)
            #acr_perrvs_rules = acr_perrvs_rules_service.create(form, acr_groups.ACR_GROUPID, acr_groups_rvs.RVSCODE)

            if acr_groups is not None and acr_groups_rvs is not None:  
                print("ACR_GROUPS created successfully") #remove after testing
                form = SAVE_RVS_FORM()
                return render(request, 'pages/acr/encoder/create-rvs.html', {'form': form})
            else:
                print("Form is not valid") #remove after testing
                print(form.errors) #remove after testing
                return render(request, 'pages/acr/encoder/create-rvs.html', {'form': form})
        
        except Exception as e:
            
            print(f"An error occurred: {e}") #remove after testing
            return render(request, 'pages/acr/encoder/create-rvs.html', {'error_message': str(e)})
    
    form = SAVE_RVS_FORM()
    return render(request, 'pages/acr/encoder/create-rvs.html', {'form': form})

def generate_acr_group_id():
    return 'CR' + str(random.randint(1000, 9999))


@approver_required
def create_icds(request):
    return render(request, 'pages/acr/encoder/create-icds.html')




