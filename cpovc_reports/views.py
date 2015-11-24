from django.shortcuts import render


def reports_home(request):
    '''
    Some default page for reports home page
    '''
    try:
        return render(request, 'reports/reports_index.html', {'status': 200})
    except Exception, e:
        raise e
