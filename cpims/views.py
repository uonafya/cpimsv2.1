from django.shortcuts import render


def home(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'dashboard.html', {'status': 200})
    except Exception, e:
        raise e


def handler_400(request):
    '''
    Some default page for Bad request error page
    '''
    try:
        return render(request, '400.html', {'status': 400})
    except Exception, e:
        raise e


def handler_404(request):
    '''
    Some default page for the Page not Found
    '''
    try:
        return render(request, '404.html', {'status': 404})
    except Exception, e:
        raise e


def handler_500(request):
    '''
    Some default page for Server Errors
    '''
    try:
        return render(request, '500.html', {'status': 500})
    except Exception, e:
        raise e
