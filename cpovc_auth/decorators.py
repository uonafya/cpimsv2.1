"""Decorator to handle permissions."""
from functools import wraps
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import available_attrs
from cpovc_registry.models import (
    RegPersonsAuditTrail, RegOrgUnitsAuditTrail, RegPersonsGeo,
    RegPersonsOrgUnits, RegOrgUnit, RegPerson)
from .perms import PERM

ORG_GROUPS = ['DEC', 'DSU', 'DUU', 'RGU']


def is_allowed_groups(allowed_groups, page=1):
    """Method for checking roles and permissions."""
    def decorator(check_func):
        @wraps(check_func, assigned=available_attrs(check_func))
        def _wrapped_view(request, *args, **kwargs):
            # If active super user lets just proceed
            print 'url', request.path_info
            page_ids = str(page).zfill(2)
            page_type = page_ids[1:]
            print page_type
            if request.user.is_active and request.user.is_superuser:
                return check_func(request, *args, **kwargs)
            else:
                level_perms = PERM[page] if page in PERM else {}
                print level_perms
                is_ovc, is_dcs, is_nat = False, False, False
                # cbo_id = request.session.get('ou_primary', 0)
                reg_ovc = request.session.get('reg_ovc', 0)
                reg_nat = request.session.get('is_national', 0)
                ou_perms = request.session.get('ou_perms', 0)
                ou_attached = request.session.get('ou_attached', 0)
                user_level = request.session.get('user_level', 0)
                print 'oup', ou_perms, ou_attached, user_level
                if level_perms['ovc'] and reg_ovc:
                    is_ovc = True
                if level_perms['dcs'] and not reg_ovc:
                    is_dcs = True
                if level_perms['ho'] and reg_nat:
                    is_nat = True
                ovc_check = (is_ovc, is_dcs, is_nat)
                from .functions import get_groups
                grps = request.user.groups.values_list('id', flat=True)
                print 'grps', grps
                cpgrp = get_groups('')
                cpims_grps = [cpgrp[grp] for grp in grps if grp in cpgrp]
                print cpims_grps
                gen_groups = [x for x in cpims_grps if x not in ORG_GROUPS]
                print ovc_check, gen_groups, cpims_grps
                response = any(value in cpims_grps for value in allowed_groups)
                if response:
                    if any(ovc_check):
                        return check_func(request, *args, **kwargs)
                # current_url = resolve(request.path_info).url_name
                page_info = 'Permission denied'
                return render(request, 'registry/roles_none.html',
                              {'page': page_info})
        return _wrapped_view
    return decorator


def is_allowed_ous(allowed_groups, page=1):
    return is_allowed_groups(allowed_groups, page)


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
