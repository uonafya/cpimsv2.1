"""CPIMS GIS module."""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def gis_home(request):
    """Method for gis."""
    try:
        return render(request, 'gis/gis_index.html',
                      {'status': 200})
    except Exception, e:
        raise e
