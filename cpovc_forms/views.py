from django.shortcuts import render


def forms_home(request):
    '''
    Some default page for forms home page
    '''
    try:
        return render(request, 'forms/forms_index.html', {'status': 200})
    except Exception, e:
        raise e
