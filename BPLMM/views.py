from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'pages/login.html')

def groups(request):
    return render(request, 'pages/acr/group-list.html')
