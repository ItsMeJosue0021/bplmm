from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'pages/login.html')

def groups(request):
    return render(request, 'pages/acr/group-list.html')

def create_rvs(request):
    return render(request, 'pages/acr/create-rvs.html')

def create_icds(request):
    return render(request, 'pages/acr/create-icds.html')

