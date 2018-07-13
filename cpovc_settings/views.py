import os
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.conf import settings

MEDIA_ROOT = settings.MEDIA_ROOT


# Create your views here.
@login_required
def settings_home(request):
    """Method to do pivot reports."""
    try:
        return render(request, 'settings/home.html', {'form': {}})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def settings_reports(request):
    """Method to do pivot reports."""
    # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime
    try:
        reports = []
        user_in = '%s-' % (request.user.id)
        directory = '%s/xlsx/' % (MEDIA_ROOT)
        for filename in os.listdir(directory):
            print filename, user_in
            is_admin = True if request.user.is_superuser else False
            is_allowed = True if filename.startswith(user_in) else is_admin
            if filename.endswith(".xlsx") and is_allowed:
                rname = os.path.join(directory, filename)
                cdate = os.stat(rname)
                (md, ino, dev, nnk, uid, gid, size, atm, mtime, ctime) = cdate
                create_date = time.ctime(mtime)
                report_name = rname.split('-')[-1]
                report = [report_name, create_date, filename]
                reports.append(report)
        return render(request, 'settings/reports.html', {'reports': reports})
    except Exception, e:
        raise e
    else:
        pass


@login_required
def archived_reports(request, file_name):
    """Method to do pivot reports."""
    try:
        directory = '%s/xlsx/' % (MEDIA_ROOT)
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
    except Exception, e:
        raise e
    else:
        pass
