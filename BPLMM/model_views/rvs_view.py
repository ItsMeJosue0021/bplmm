import random
from django.db.models import Q # type: ignore
from datetime import datetime
from django.contrib import messages # type: ignore
from django.core.paginator import Paginator # type: ignore
from ..forms import SAVE_RVS_FORM
from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from ..decorators import encoder_required, approver_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
#services
from ..services.rvs_service import ACR_GROUPS_RVS_SERVICE
#repositories
from ..repositories.rvs_repository import ACR_GROUPS_RVS_REPOSITORY

acr_groups_rvs_service = ACR_GROUPS_RVS_SERVICE(ACR_GROUPS_RVS_REPOSITORY())

@login_required
@encoder_required
def rvs_create_modal(request, group_id):
    template = 'components/acr/fieldsets/acr-rvs.html'
    form = SAVE_RVS_FORM(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data
            try:
                acr_groups_rvs = acr_groups_rvs_service.create_temp_modal(data, group_id, request)
                if acr_groups_rvs is not None:  
                    form = SAVE_RVS_FORM()
                    messages.success(request, 'RVS has been saved successfully.')
                    return render(request, template, {'form': form, 'group_id': group_id})
                else:
                    raise Exception('An error occurred while saving RVS.')
            except Exception as e:
                messages.error(request, str(e))
        else:
             messages.error(request, 'Please make sure all fields are filled out.')
    return render(request, template, {'form': form, 'group_id': group_id})