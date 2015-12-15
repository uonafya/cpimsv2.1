import re
from functools import wraps
from django.shortcuts import render
from django.utils.decorators import available_attrs

ORG_GROUPS = ['DEC', 'DSU', 'DUU', 'RGU']

ORGS_TEXT = {'registry/new': 'Create new Organisational unit.',
             'registry/edit': 'Edit Organisational unit.',
             'registry/view': 'View Organisational unit details.'}

COUNTY_TEXT = {}


def is_allowed_groups(allowed_groups):
    def decorator(check_func):
        @wraps(check_func, assigned=available_attrs(check_func))
        def _wrapped_view(request, *args, **kwargs):
            from .functions import get_groups, get_allowed_units_county
            # None restrictive roles
            grps = request.user.groups.values_list('id', flat=True)
            cpims_grp = get_groups('')
            # Get org units and sub-counties
            user_id = request.user.id
            current_uri = request.path_info
            ex_areas, ex_orgs = get_allowed_units_county(user_id)
            ogrps = allowed_org_county(ex_areas, ex_orgs, current_uri)
            # Do the check now for non-restrictive groups
            cpims_groups = [cpims_grp[grp] for grp in grps if grp in cpims_grp]
            gen_groups = [x for x in cpims_groups if x not in ORG_GROUPS]
            response = any(value in gen_groups for value in allowed_groups)
            # Do the check now for org unit and sub-county
            org_check = False
            if ogrps:
                ogroups = [cpims_grp[grp] for grp in ogrps if grp in cpims_grp]
                org_check = any(value in ogroups for value in allowed_groups)
            if response or org_check:
                return check_func(request, *args, **kwargs)
            else:
                from django.core.urlresolvers import resolve
                current_url = resolve(request.path_info).url_name
                pg_exists = current_url in ORGS_TEXT
                page_info = ORGS_TEXT[current_url] if pg_exists else 'details'
                return render(request, 'registry/roles_none.html',
                              {'page': page_info})
        return _wrapped_view
    return decorator


def allowed_org_county(areas, orgs, cur_url):
    '''
    Method to try decipher url and determine id being requested
    Then also check if it is an org unit or its an area
    '''
    try:
        group_orgs = None
        for org_text in ORGS_TEXT:
            match_org = re.match(r"^(.?)/%s/(\d+)(.?)$" % (org_text), cur_url)
            if match_org:
                org_unit = int(match_org.group(2))
                if org_unit in orgs:
                    group_orgs = orgs[org_unit]
        if group_orgs:
            return group_orgs
    except Exception, e:
        error = "Error in getting allowed org units / county - %s" % (str(e))
        print error
        return False
    else:
        return False
