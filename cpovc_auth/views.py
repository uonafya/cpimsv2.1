from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from cpovc_auth.forms import LoginForm, RegistrationForm
from cpovc_auth.models import AppUser


def home(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'base.html', {'status': 200})
    except Exception, e:
        raise e


def log_in(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        form = LoginForm(data=request.POST)
        if request.method == 'POST':
            if form.is_valid():
                username = form.data['username'].strip()
                password = form.data['password'].strip()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # grps = user.groups.all()
                        return HttpResponseRedirect('/')
                    else:
                        msg = "Login Account is currently disabled."
                        return render(request, 'login.html',
                                      {'form': form, 'msg': msg})
                else:
                    msg = "Incorrect username and / or password."
                    return render(request, 'login.html', {'form': form,
                                  'msg': msg})
        else:
            logout(request)
        return render(request, 'login.html', {'form': form, 'status': 200})
    except Exception, e:
        raise e


def register(request):
    '''
    Some default page for the home page / Dashboard
    '''
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_no = form.cleaned_data['phone_no']
            national_id = form.cleaned_data['national_id']
            list_geolocation_id = form.cleaned_data['list_geolocation_id']
            staff_no = form.cleaned_data['staff_no']

            now = timezone.now()
            AppUser(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_no=phone_no,
                national_id=national_id,
                list_geolocation_id=list_geolocation_id,
                staff_no=staff_no,
                is_staff=False,
                is_active=True,
                is_superuser=False,
                last_login=now,
                date_joined=now, ).save()
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form},)
