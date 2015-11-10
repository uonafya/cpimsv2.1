from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from cpovc_auth.forms import LoginForm


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
    Method to handle log in to system
    '''
    try:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
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
            form = LoginForm()
            logout(request)
        return render(request, 'login.html', {'form': form, 'status': 200})
    except Exception, e:
        raise e


def log_out(request):
    '''
    Method to handle log out to system
    '''
    try:
        print "User [%s] successfully logged out." % (request.user.username)
        logout(request)
        return HttpResponseRedirect('/')
    except Exception, e:
        raise e


def register(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'register.html', {'status': 200})
    except Exception, e:
        raise e
