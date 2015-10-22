from django.shortcuts import render


def home(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'index.html', {'foo': 'bar'})
    except Exception, e:
        raise e
