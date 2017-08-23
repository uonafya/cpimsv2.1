"""Decorator to handle permissions."""
import re
from functools import wraps
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import available_attrs
from django.core.urlresolvers import resolve
from cpovc_registry.models import (
    RegPersonsAuditTrail, RegOrgUnitsAuditTrail, RegPersonsGeo,
    RegPersonsOrgUnits, RegOrgUnit, RegPerson)
from cpovc_auth.models import AppUser

ORG_GROUPS = ['DEC', 'DSU', 'DUU', 'RGU']

ORGS_TEXT = {'registry/new/': 'Create new Organisational unit.',
             'registry/edit/': 'Edit Organisational unit.',
             'registry/view/': 'View Organisational unit details.',
             'registry/new_person/': 'Register a new person.',
             'registry/edit_person/': 'Edit existing person.',
             'registry/view_person/': 'View person details.',
             'auth/roles/': 'Manage roles',
             'registry/new_user/': 'Create a new login account.'}

COUNTY_TEXT = {}
ALLOWED_PAGES = ['registry/new', 'registry/new_person', 'registry/new_user']
ALLOWED_OWN = ['registry/edit', 'registry/edit_person']


def is_allowed_ous(allowed_groups, page=1):
    """Method for checking roles and permissions."""
    def decorator(check_func):
        @wraps(check_func, assigned=available_attrs(check_func))
        def _wrapped_view(request, *args, **kwargs):
            # If active super user lets just proceed
            print 'url', request.path_info
            if request.user.is_active and request.user.is_superuser:
                return check_func(request, *args, **kwargs)
            else:
                from .functions import get_groups
                grps = request.user.groups.values_list('id', flat=True)
                cpgrp = get_groups('')
                cpims_grps = [cpgrp[grp] for grp in grps if grp in cpgrp]
                gen_groups = [x for x in cpims_grps if x not in ORG_GROUPS]
                response = any(value in gen_groups for value in allowed_groups)
                if response:
                    return check_func(request, *args, **kwargs)
                current_url = resolve(request.path_info).url_name
                pg_exists = current_url in ORGS_TEXT
                page_info = ORGS_TEXT[current_url] if pg_exists else 'details'
                return render(request, 'registry/roles_none.html',
                              {'page': page_info})
        return _wrapped_view
    return decorator


def is_allowed_groups(allowed_groups):
    """Method for checking roles and permissions."""
    def decorator(check_func):
        @wraps(check_func, assigned=available_attrs(check_func))
        def _wrapped_view(request, *args, **kwargs):
            # If active super user lets just proceed
            if request.user.is_active and request.user.is_superuser:
                return check_func(request, *args, **kwargs)
            from .functions import get_groups, get_allowed_units_county
            # None restrictive roles
            grps = request.user.groups.values_list('id', flat=True)
            cpims_grp = get_groups('')
            # Get org units and sub-counties
            user_id = request.user.id
            ex_areas, ex_orgs = get_allowed_units_county(user_id)
            ogrps, pgrps = allowed_org_county(ex_areas, ex_orgs, request)
            print ogrps, pgrps, grps, ex_orgs
            # Do the check now for non-restrictive groups
            cpims_groups = [cpims_grp[grp] for grp in grps if grp in cpims_grp]
            gen_groups = [x for x in cpims_groups if x not in ORG_GROUPS]
            response = any(value in gen_groups for value in allowed_groups)
            # Do the check now for org unit and sub-county
            org_check, allow_create = False, False
            if ogrps:
                ogroups = [cpims_grp[grp] for grp in ogrps if grp in cpims_grp]
                org_check = any(value in ogroups for value in allowed_groups)
            # These urls
            orgp_grps = [3, 7]
            org_person = any(value in orgp_grps for value in grps)
            cur_url = request.path_info.strip("/")
            # cur_url = re.sub('\d', '', curr_url)
            if org_person and cur_url in ALLOWED_PAGES:
                allow_create = True
            print 'ROLES', response, org_check
            if response or org_check or allow_create or pgrps:
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


def allowed_org_county(areas, orgs, request):
    """
    Method to try decipher url and determine id being requested.

    Then also check if it is an org unit or its an area
    """
    try:
        org_url = None
        cur_url = request.path_info
        group_orgs, all_persons = None, None
        person_id, item_id = 0, 0
        plain_url = cur_url.lstrip("/")
        for org_text in ORGS_TEXT:
            if plain_url.startswith(org_text):
                org_url = org_text
        if org_url:
            print 'CUR URL', org_url
            match_org = re.match(r"^(.?)/%s(\d+)(.?)$" % (org_url), cur_url)
            if match_org:
                item_id = int(match_org.group(2))
                if 'person' in cur_url or 'user' in cur_url:
                    person_id = item_id
                if 'auth' in cur_url:
                    person_id = get_user_ids(request, item_id)
                else:
                    if item_id in orgs:
                        group_orgs = orgs[item_id]
            all_persons = get_person_ids(request, person_id, item_id)
        return group_orgs, all_persons
    except Exception, e:
        error = "Error in getting allowed org units / county - %s" % (str(e))
        print error
        return False


def get_user_ids(request, user_id):
    """Method to get person id from user id."""
    try:
        person_obj = AppUser.objects.get(id=user_id)
        person_id = person_obj.reg_person_id
        return person_id
    except Exception:
        pass


def get_person_ids(request, person_id, item_id):
    """Method to get person ids in area and org unit of jurisdiction."""
    try:
        # user_id = request.user.id
        # cur_url = request.path_info.strip("/")
        cur_person_id = request.user.reg_person_id
        cur_user_id = request.user.id
        if person_id == cur_person_id:
            return [person_id]
        # Determine who created this record from Persons audit trail
        if person_id and person_id == item_id:
            print 'Here in Persons'
            record_details = get_creator_details(person_id)
            if record_details:
                creator_id = record_details.created_by.pk
                creator_pid = record_details.created_by.reg_person_id
                print 'person ids', creator_id, person_id
                if creator_id == cur_user_id:
                    return [creator_id]
                # Determine if these two work in the same org unit
                # For Government, NGO and Volunteer
                org_units = check_workmate(creator_pid, cur_person_id)
                if org_units:
                    return org_units
            else:
                # If Child / Caregiver check if its same area of jurisdiction
                print 'This is a fellow staff member.'
                # I did not create but we work in same organisation
                check_wm = check_workmate(person_id, cur_person_id)
                return check_wm

        else:
            # Determine who created this record from Org Units audit trail
            if item_id and not person_id:
                print 'Here in Org Units'
                record_details = get_audit_details(item_id, 'Unit')
                if record_details:
                    creator_id = record_details.app_user_id
                    if creator_id == cur_user_id:
                        return [creator_id]
                    # Determine if they work in the same org unit.
                    org_units = check_workmate(creator_pid, cur_person_id, 'U')
                    if org_units:
                        return org_units
            else:
                print 'Here in Roles management'
                check_wm = check_workmate(person_id, cur_person_id)
                return check_wm
        return []
    except Exception, e:
        print 'Error - %s' % (str(e))
        pass
    else:
        return []


def get_creator_details(item_id, audit_type='Person'):
    """Method to query audit trail for creator."""
    try:
        if audit_type == 'Person':
            record_details = get_object_or_404(
                RegPerson.objects.select_related(), pk=item_id)
        else:
            record_details = get_object_or_404(
                RegOrgUnit.objects.select_related(), pk=item_id)
        return record_details
    except Exception:
        return None


def get_audit_details(item_id, audit_type='Person'):
    """Method to query audit trail for creator."""
    try:
        if audit_type == 'Person':
            record_details = get_object_or_404(
                RegPersonsAuditTrail.objects.select_related(),
                person_id=item_id, transaction_type_id='REGS')
        else:
            record_details = get_object_or_404(
                RegOrgUnitsAuditTrail.objects.select_related(),
                org_unit_id=item_id, transaction_type_id='REGU')
        return record_details
    except Exception:
        return None


def check_workmate(creator_id, cur_person_id, check_type='P'):
    """Method to check if they belong to same org unit."""
    try:
        orgs_dict = {creator_id: [], cur_person_id: []}
        geos_dict = {creator_id: [], cur_person_id: []}
        person_ids = [creator_id, cur_person_id]
        person_orgs = RegPersonsOrgUnits.objects.select_related().filter(
            person_id__in=person_ids, is_void=False, date_delinked=None)
        if check_type == 'P':
            person_details = RegPersonsGeo.objects.select_related().filter(
                person_id__in=person_ids, is_void=False, date_delinked=None)

            for person_detail in person_details:
                area_id = person_detail.area_id
                geos_dict[person_detail.person_id].append(area_id)

        for person_org in person_orgs:
            orgs_dict[person_org.person_id].append(person_org.org_unit_id)

        print 'B4 Check', orgs_dict, geos_dict
        creator_org = set(orgs_dict[creator_id])
        user_org = set(orgs_dict[cur_person_id])

        same_orgs = creator_org.intersection(user_org)
        if same_orgs:
            return list(same_orgs)
        # Check geo
        creator_geo = set(geos_dict[creator_id])
        user_geo = set(geos_dict[cur_person_id])
        same_geo = creator_geo.intersection(user_geo)
        if same_geo:
            return list(same_geo)
        return []
    except Exception, e:
        print 'error - %s' % (str(e))
        return None
