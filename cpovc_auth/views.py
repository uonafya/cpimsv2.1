from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from cpovc_auth.forms import LoginForm
from cpims.views import home

def auth_home(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'base.html', {'status': 200})
    except Exception, e:
        raise e


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        try:
            if form.is_valid():
                username = form.data['username'].strip()
                password = form.data['password'].strip()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse(home))
                    else:
                        msg = "Login Account is currently disabled."
                        messages.add_message(request, messages.INFO, msg)
                        return render(request, 'login.html',
                                      {'form': form})
                else:
                    msg = "Incorrect username and / or password."
                    messages.add_message(request, messages.INFO, msg)
                    return render(request, 'login.html', {'form': form})
        except Exception, e:
            msg = 'Login error - %s' % (str(e))
            messages.add_message(request, messages.INFO, msg)
        return render(request, 'login.html', {'form': form,})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form,})


def log_out(request):
    '''
    Method to handle log out to system
    '''
    try:
        print "User [%s] successfully logged out." % (request.user.username)
        logout(request)
        return HttpResponseRedirect(reverse(home))
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
