from django.contrib.auth import authenticate, login, logout # type: ignore

class AUTH_SERVICE:
  
    def authenticate_user(request, username, password):
        return authenticate(request, username=username, password=password)
    
    def login_user(request, user):
        login(request, user)
    
    def logout_user(request):
        logout(request)    
        
    def authenticated_redirect(user):
        if user.groups.filter(name='Encoder').exists():
            return 'acr'
        elif user.groups.filter(name='Approver').exists():
            return 'approver_pending_groups_list'
        else:
            return 'login'