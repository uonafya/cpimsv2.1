"""Registry common functions."""
import uuid
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from cpovc_main.models import SetupGeography, SetupList, RegTemp
from cpovc_main.functions import convert_date, get_dict
from django.db.models import Q, Count
from .models import (
    RegOrgUnitContact, RegOrgUnit, RegOrgUnitExternalID, RegOrgUnitGeography,
    RegPersonsOrgUnits, RegPersonsExternalIds, RegPerson, RegPersonsGeo,
    RegPersonsTypes, RegPersonsSiblings, RegPersonsAuditTrail, AppUser,
    RegOrgUnitsAuditTrail)

from cpovc_auth.models import CPOVCUserRoleGeoOrg
from cpovc_forms.models import OVCCaseRecord, OVCCaseCategory

organisation_id_prefix = 'U'
benficiary_id_prefix = 'B'
workforce_id_prefix = 'W'


def dashboard():
    """Method to get dashboard totals."""
    try:
        dash = {}
        vals = {'TBVC': 0, 'TBGR': 0, 'TWGE': 0, 'TWNE': 0}
        person_types = RegPersonsTypes.objects.filter(
            is_void=False, date_ended=None).values(
                'person_type_id').annotate(dc=Count('person_type_id'))
        for person_type in person_types:
            vals[person_type['person_type_id']] = person_type['dc']
        dash['children'] = vals['TBVC']
        dash['guardian'] = vals['TBGR']
        dash['government'] = vals['TWGE']
        dash['ngo'] = vals['TWNE']
        # Get org units
        org_units = RegOrgUnit.objects.filter(is_void=False).count()
        dash['org_units'] = org_units
        # Case records counts
        case_records = OVCCaseRecord.objects.filter(is_void=False)
        case_counts = case_records.count()
        dash['case_records'] = case_counts
        # Workforce members
        workforce_members = RegPersonsExternalIds.objects.filter(
            identifier_type_id='IWKF', is_void=False).count()
        dash['workforce_members'] = workforce_members
        # Case categories to find pending cases
        pending_cases = OVCCaseCategory.objects.filter(
            is_void=False)
        pending_count = pending_cases.exclude(
            case_id__summon_status=True).count()
        dash['pending_cases'] = pending_count
        # Child registrations
        ptypes = RegPersonsTypes.objects.filter(
            person_type_id='TBVC', is_void=False,
            date_ended=None).values_list('person_id', flat=True)
        cregs = RegPerson.objects.filter(id__in=ptypes).values(
            'created_at').annotate(unit_count=Count('created_at'))
        child_regs, case_regs = {}, {}
        for creg in cregs:
            the_date = creg['created_at']
            cdate = the_date.strftime('%d-%b-%y')
            child_regs[str(cdate)] = creg['unit_count']
        # Case Records
        ovc_regs = case_records.values(
            'date_case_opened').annotate(unit_count=Count('date_case_opened'))
        for ovc_reg in ovc_regs:
            the_date = ovc_reg['date_case_opened']
            cdate = the_date.strftime('%d-%b-%y')
            case_regs[str(cdate)] = ovc_reg['unit_count']
        # Case categories Top 5
        case_categories = pending_cases.values(
            'case_category').annotate(unit_count=Count(
                'case_category')).order_by('-unit_count')
        dash['child_regs'] = child_regs
        dash['case_regs'] = case_regs
        dash['case_cats'] = case_categories
    except Exception:
        pass
    else:
        return dash


def get_temp(request):
    """Method to get last temp data only less than 15 minutes old."""
    try:
        user_id = request.user.id
        page_id = request.get_full_path()
        print "CHECK TMP", user_id, page_id
        time_threshold = timezone.now() - timedelta(minutes=15)
        tmps = RegTemp.objects.get(user_id=user_id, page_id=page_id,
                                   created_at__gt=time_threshold)
        if tmps:
            return eval(tmps.data)
        return {}
    except Exception:
        return {}


def unit_duplicate(request):
    """Method to check if same unit exists with same name."""
    resp = {'status': 0}
    try:
        print 'DUP org check', request.POST
        unit_name = request.POST.get('org_unit_name').strip()
        existing_units = RegOrgUnit.objects.filter(
            org_unit_name__iexact=unit_name, is_void=False).count()
        resp['status'] = existing_units
        return resp
    except Exception, e:
        print "Error checking unit duplicate - %s" % (str(e))
        return {'status': 9}


def person_duplicate(request, person='child'):
    """Method to check if child already exists."""
    resp = {'status': 0}
    try:
        print 'DUP Check', request.POST
        if person == 'sibling':
            first_name = request.POST.get('sibling_firstname').strip()
            surname = request.POST.get('sibling_surname').strip()
            other_names = request.POST.get('sibling_othernames').strip()
            date_of_birth = request.POST.get('sibling_dob')
            gender = request.POST.get('sibling_gender')
        else:
            first_name = request.POST.get('first_name').strip()
            surname = request.POST.get('surname').strip()
            other_names = request.POST.get('other_names').strip()
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('sex_id')
        sub_county = request.POST.get('living_in_subcounty')
        ward = request.POST.get('living_in_ward')
        if not date_of_birth or len(str(date_of_birth)) != 10:
            date_of_birth = None
        else:
            date_of_birth = convert_date(date_of_birth)
        children_qs = RegPerson.objects.filter(
            first_name__iexact=first_name, surname__iexact=surname,
            date_of_birth=date_of_birth, sex_id=gender, is_void=False)
        if other_names:
            children_qs = children_qs.filter(
                other_names_iexact=other_names)
        # Check in Geo locations
        pers_geo = RegPersonsGeo.objects.filter(
            area_id=sub_county, is_void=False)
        pers_geo = pers_geo.values_list("person__id")
        children_qs = children_qs.filter(id__in=pers_geo)
        if ward:
            ward_geo = RegPersonsGeo.objects.filter(
                area_id=ward, is_void=False)
            ward_geo = ward_geo.values_list("person__id")
            children_qs = children_qs.filter(id__in=ward_geo)
        if children_qs:
            resp['status'] = children_qs.count()
            resp['child'] = children_qs
        return resp
    except Exception, e:
        print 'Error checking child duplicate - %s' % (str(e))
        return {'status': 9}


def get_list_types(list_type=['organisation_type_id']):
    """Method to get all organisation types for js."""
    try:
        org_units = SetupList.objects.filter(is_void=False)
        vals = []
        orgs = {}
        orgs_dict = {}
        cnt = 0
        for org_unit in org_units:
            field_name = org_unit.field_name
            item_sub_cat = org_unit.item_sub_category
            res = {'id': org_unit.item_id, 'name': org_unit.item_description,
                   'cat': item_sub_cat, 'field_name': field_name}
            vals.append(res)
            if org_unit.field_name in list_type:
                cnt += 1
                blks = 'BLK_%s' % (str(cnt))
                item_scat = item_sub_cat if item_sub_cat else blks
                orgs[item_scat] = org_unit.item_id
        for val in vals:
            val_field = val['field_name']
            if val_field in orgs:
                type_id = str(orgs[val_field])
                type_id_name = '%s,%s' % (str(val['id']), str(val['name']))
                if type_id not in orgs_dict:
                    orgs_dict[type_id] = [type_id_name]
                else:
                    orgs_dict[type_id].append(type_id_name)
        for org in orgs:
            if org.startswith('BLK_'):
                org_id = orgs[org]
                orgs_dict[org_id] = []
        return orgs_dict
    except Exception, e:
        print 'error - %s' % (str(e))
        pass


def get_user_geos(user):
    """Get attached user Geos."""
    try:
        user_id = user.id
        sub_counties = []
        results = {'sub_counties': [], 'counties': [], 'wards': []}
        user_geos = CPOVCUserRoleGeoOrg.objects.select_related().filter(
            is_void=False, user_id=user_id, area_id__isnull=False)
        print "CHECK", user_geos, user_id
        for user_geo in user_geos:
            geo_id = user_geo.area_id
            sub_counties.append(geo_id)
        if sub_counties:
            # Get all counties if in this list of sub-counties
            wards = []
            counties = counties_from_aids(sub_counties)
            results['sub_counties'] = sub_counties
            results['counties'] = counties
            # Get all counties if in this list of sub-counties
            if counties:
                wards = geos_from_aids(sub_counties, area_type='GWRD')
            results['wards'] = wards
        return results
    except Exception:
        pass


def get_user_details(person):
    """Method to get account user details."""
    try:
        person_appuser = AppUser.objects.get(
            reg_person=person, is_active=True)
        return person_appuser
    except Exception, e:
        print "Get user details error - %s" % (str(e))
        return None


def counties_from_aids(area_list, area_type='GDIS'):
    """Method to get counties for display from area ids."""
    try:
        geos = SetupGeography.objects.filter(
            area_id__in=area_list, area_type_id=area_type,
            is_void=False).values_list('parent_area_id', flat=True)
    except Exception, e:
        print 'Error getting county list from area ids - %s' % (str(e))
        return []
    else:
        return geos


def geos_from_aids(area_list, area_type='GWRD'):
    """Method to get wards from sub-counties for display from area ids."""
    try:
        geos = SetupGeography.objects.filter(
            parent_area_id__in=area_list, area_type_id=area_type,
            is_void=False).values_list('area_id', flat=True)
    except Exception, e:
        print 'Error getting county list from area ids - %s' % (str(e))
        return []
    else:
        return geos


def create_geo_list(geo_dict, form_items, geo_type='GLTW'):
    """Method to create a big dict for saving all geo locations."""
    try:
        if form_items:
            for geo_item in form_items:
                if geo_item:
                    geo_dict[int(geo_item)] = geo_type
    except Exception, e:
        print 'Error creating persons geos - %s' % (str(e))
        return geo_dict
    else:
        return geo_dict


def save_audit_trail(request, params, audit_type='Person'):
    """Method to save audit trail depending on transaction."""
    try:
        user_id = request.user.id
        ip_address = get_client_ip(request)
        transaction_type_id = params['transaction_type_id']
        interface_id = params['interface_id']
        meta_data = get_meta_data(request)
        paper_date = None
        print 'Audit Trail', params
        if len(params) >= 3 and audit_type == 'Person':
            date_recorded_paper = params['date_recorded_paper']
            paper_person_id = params['paper_person_id']
            if not paper_person_id:
                paper_person_id = user_id
            person_id = params['person_id']
            if date_recorded_paper:
                paper_date = convert_date(date_recorded_paper)
            RegPersonsAuditTrail(
                transaction_type_id=transaction_type_id,
                interface_id=interface_id,
                date_recorded_paper=paper_date,
                person_recorded_paper_id=paper_person_id,
                timestamp_modified=None,
                app_user_id=user_id,
                ip_address=ip_address,
                meta_data=meta_data,
                person_id=person_id).save()
        elif audit_type == 'Unit':
            org_unit_id = params['org_unit_id']
            RegOrgUnitsAuditTrail(
                transaction_type_id=transaction_type_id,
                interface_id=interface_id,
                timestamp_modified=None,
                org_unit_id=org_unit_id,
                ip_address=ip_address,
                meta_data=meta_data,
                app_user_id=user_id).save()
    except Exception, e:
        print 'Error saving audit - %s' % (str(e))
        pass
    else:
        pass


def save_sibling(request, attached_sb, person_id):
    """Method to save siblings in some weird manner."""
    try:
        new_sib_ids = []
        for sib_id in attached_sb:
            if len(attached_sb[sib_id]) > 4:
                sibling_fdob = attached_sb[sib_id]['dob']
                sibling_names = attached_sb[sib_id]['names'].split('|')
                sibling_rmk = attached_sb[sib_id]['rmk']
                sibling_sex = attached_sb[sib_id]['sex']
                sibling_first_name = sibling_names[0].upper()
                sibling_surname = sibling_names[1].upper()
                sibling_othernames = sibling_names[2].upper()
                sibling_cpid = attached_sb[sib_id]['sbid']
                # To be used by the education background form
                # sibling_class = attached_sb[sib_id]['slevel']
                # Convert date to db one here
                is_dob = None if len(str(sibling_fdob)) != 11 else True
                sibling_dob = convert_date(sibling_fdob) if is_dob else None
                if sibling_cpid:
                    sibling_id = int(sibling_cpid)
                else:
                    # Save as a person if has no sibling id
                    person = RegPerson(
                        designation='',
                        first_name=sibling_first_name.upper(),
                        other_names=sibling_othernames.upper(),
                        surname=sibling_surname.upper(),
                        sex_id=sibling_sex, date_of_birth=sibling_dob,
                        des_phone_number=None, email='',
                        created_by_id=request.user.id,
                        is_void=False)
                    person.save()
                    sibling_id = person.pk
                    # Save this person type
                    person_types = ['TBVC']
                    save_person_type(person_types, sibling_id)
                todate = timezone.now()

                nsib, created = RegPersonsSiblings.objects.update_or_create(
                    child_person_id=person_id, is_void=False,
                    sibling_person_id=sibling_id,
                    defaults={'child_person_id': person_id,
                              'sibling_person_id': sibling_id,
                              'date_linked': todate, 'remarks': sibling_rmk,
                              'is_void': False},)
                # Use Owners location details to create/update sibling details
                copy_locations(person_id, sibling_id)
                new_sib_ids.append(sibling_id)
                # Audit trail required here for tracking creators
                params = {}
                params['transaction_type_id'] = 'REGS'
                params['interface_id'] = 'INTW'
                params['date_recorded_paper'] = None
                params['paper_person_id'] = None
                params['person_id'] = int(sibling_id)
                save_audit_trail(request, params)
    except Exception, e:
        print 'Error attaching sibling - ', str(e)
        pass
    else:
        return new_sib_ids


def copy_locations(person_id, relative_id):
    """Method to copy owners locations to sibling / guardian."""
    try:
        todate = timezone.now()
        owner_locations = RegPersonsGeo.objects.filter(
            is_void=False, date_delinked=None, person_id=person_id)
        if owner_locations:
            for oloc in owner_locations:
                area_id = oloc.area_id
                area_type = oloc.area_type
                nloc, created = RegPersonsGeo.objects.update_or_create(
                    person_id=relative_id, area_id=area_id, is_void=False,
                    defaults={'area_id': area_id,
                              'person_id': relative_id,
                              'area_type': area_type,
                              'date_linked': todate,
                              'is_void': False},)
    except Exception, e:
        raise e


def save_person_extids(identifier_types, person_id):
    """Save Person external ids details - Create or update."""
    try:
        for identifier_type in identifier_types:
            identifier = identifier_types[identifier_type]
            location, created = RegPersonsExternalIds.objects.update_or_create(
                person_id=person_id, identifier_type_id=identifier_type,
                is_void=False,
                defaults={'person_id': person_id, 'identifier': identifier,
                          'identifier_type_id': identifier_type,
                          'is_void': False},)
    except Exception, e:
        raise e
    else:
        pass


def save_person_type(person_types, person_id):
    """Method to save all person types."""
    try:
        now = timezone.now()
        for i, p_type in enumerate(person_types):
            RegPersonsTypes(
                person_id=person_id,
                person_type_id=p_type,
                date_began=now,
                date_ended=None,
                is_void=False).save()
    except Exception, e:
        raise e
    else:
        pass


def remove_person_type(person_types, person_id):
    """To mark as removed all person types - date_ended."""
    try:
        now = timezone.now()
        for i, type_id in enumerate(person_types):
            person_area = get_object_or_404(
                RegPersonsTypes, pk=type_id,
                person_id=person_id, is_void=False)
            person_area.date_ended = now
            person_area.save(update_fields=["date_ended"])
    except Exception, e:
        raise e
    else:
        pass


def save_locations(area_ids, person_id):
    """Save locations details."""
    try:
        now = timezone.now()
        for area_id in area_ids:
            area_type = area_ids[area_id]
            RegPersonsGeo(
                person_id=person_id,
                area_id=area_id,
                area_type=area_type,
                date_linked=now,
                date_delinked=None,
                is_void=False).save()
    except Exception, e:
        raise e
    else:
        pass


def remove_locations(area_ids, person_id):
    """Save locations details."""
    try:
        now = timezone.now()
        for area_id in area_ids:
            person_area = get_object_or_404(
                RegPersonsGeo, pk=area_id, person_id=person_id, is_void=False)
            person_area.date_delinked = now
            person_area.is_void = True
            person_area.save(update_fields=["date_delinked", "is_void"])
    except Exception, e:
        raise e
    else:
        pass


def names_from_ids(ids, registry='orgs'):
    """Method to return geo names from list of ids."""
    try:
        orgs = get_specific_geos(ids, registry, reg_type=['GDIS'])
        orgs_name = {}
        # For getting all area names comma separated
        for geo in ids:
            if geo in orgs:
                gname = orgs[geo]
                orgs_name[geo] = ', '.join(gname)
            else:
                orgs_name[geo] = None
    except Exception, e:
        print 'Error getting list - %s' % (str(e))
        return None
    else:
        return orgs_name


def merge_two_dicts(dict_x, dict_y):
    """
    Given two dicts, merge them into a new dict.

    Uses a shallow copy.
    """
    new_dict = dict_x.copy()
    new_dict.update(dict_y)
    return new_dict


def auto_suggest_person(request, query, qid=0):
    """
    Auto suggest method using jquery auto-suggest.

    Return values are json with extra
    parameters for siblings and caregivers
    """
    try:
        results = []
        person_type = 'TBGR'
        query_id = int(request.GET.get('id'))
        # Get the filter ids
        query_ids = {0: 'TBGR', 1: 'TBVC', 2: 'IWKF'}
        detail_list = [0, 1]
        if query_id in query_ids:
            person_type = query_ids[query_id]
        # Filters for external ids
        if query_id in [0, 1]:
            person_ids = RegPersonsTypes.objects.filter(
                person_type_id=person_type, is_void=False).values_list(
                    'person_id', flat=True)
        else:
            wf_ids = ['TWNE', 'TWGE', 'TWVL']
            person_ids = RegPersonsTypes.objects.filter(
                person_type_id__in=wf_ids, is_void=False).values_list(
                    'person_id', flat=True)
        queryset = RegPerson.objects.filter(
            id__in=person_ids, is_void=False)
        field_names = ['surname', 'email', 'first_name', 'other_names']
        q_filter = Q()
        for field in field_names:
            q_filter |= Q(**{"%s__icontains" % field: query})
        persons = queryset.filter(q_filter)
        for person in persons:
            person_id = person.pk
            name = '%s %s %s' % (person.first_name, person.surname,
                                 person.other_names)
            val = {'id': person.pk, 'label': name, 'value': name}
            if query_id in detail_list:
                person_dob = person.date_of_birth
                if person_dob:
                    dob_dateobj = convert_date(str(person_dob), '%Y-%m-%d')
                    person_dob = dob_dateobj.strftime('%d-%b-%Y')
                val['gender'] = person.sex_id
                val['dob'] = person_dob
                val['fname'] = person.first_name
                val['sname'] = person.surname
                val['onames'] = person.other_names
            if qid == 1:
                # Get case records belonging to this child
                cases = []
                all_cases = OVCCaseRecord.objects.filter(
                    is_void=False, person_id=person_id)
                for case in all_cases:
                    case_date = case.date_case_opened.strftime('%d-%b-%Y')
                    cd = {'id': case.case_id, 'serial': str(case.case_serial),
                          'case_date': case_date}
                    cases.append(cd)
                if cases:
                    val['cases'] = cases
                val['label'] = '%s (%s)' % (name, len(cases))
            results.append(val)
    except Exception, e:
        print 'error checking persons - %s' % (str(e))
        return []
    else:
        return results


def extract_post_params(request, naming='cc_'):
    """Extract from POST params values starting with some naming."""
    try:
        reqs = request.POST
        req_vals = {}
        for req in reqs:
            val = request.POST.get(req).strip()
            if req.startswith(naming):
                vals = req.split('_')
                if len(vals) > 2:
                    cid, cvalue = vals[1], vals[2]
                    if cid not in req_vals:
                        req_vals[cid] = {}
                    if len(req_vals) > 0:
                        req_vals[cid][cvalue] = val
                    else:
                        req_vals[cid] = {cvalue: val}
                else:
                    cid = vals[1]
                    req_vals[cid] = val.split(',')
        return req_vals
    except Exception, e:
        raise e


def create_olists(org_lists, org_detail, org_ids, ltype=0):
    """Method to create org list of units, sub-units and sub-sub-units."""
    try:
        if ltype == 0:
            for org_list in org_lists:
                unit_id = org_list.org_unit.id
                unit_vis = org_list.org_unit.org_unit_id_vis
                unit_name = org_list.org_unit.org_unit_name
                unit_names = '%s - %s' % (unit_vis, unit_name)
                org_detail[unit_id] = unit_names
                org_ids.append(unit_id)
        else:
            for org_list in org_lists:
                unit_id = org_list.id
                unit_vis = org_list.org_unit_id_vis
                unit_name = org_list.org_unit_name
                unit_names = '%s - %s' % (unit_vis, unit_name)
                org_detail[unit_id] = unit_names
                org_ids.append(unit_id)
    except Exception, e:
        raise e
    else:
        return org_detail, org_ids


def get_specific_orgs(user_id):
    """Get specific Organisational units based on user id."""
    org_detail, result = {'': 'Select Parent Unit'}, ()
    try:
        org_ids = []
        org_lists = RegPersonsOrgUnits.objects.select_related().filter(
            person_id=user_id, is_void=False)
        if org_lists:
            org_detail, org_ids = create_olists(org_lists, org_detail, org_ids)
            # Get sub units
            sub_results = RegOrgUnit.objects.select_related().filter(
                parent_org_unit_id__in=org_ids, is_void=False)
            if sub_results:
                org_detail, sub_org_ids = create_olists(
                    sub_results, org_detail, org_ids, 1)
                # Get sub sub units
                ssub_results = RegOrgUnit.objects.select_related().filter(
                    parent_org_unit_id__in=sub_org_ids, is_void=False)
                if ssub_results:
                    org_detail, ssub_org_ids = create_olists(
                        ssub_results, org_detail, org_ids, 2)
        result = org_detail.items()
    except Exception, e:
        error = 'Error getting specific orgs - %s' % (str(e))
        print error
        return result
    else:
        return result


def get_specific_geos(list_ids, registry='orgs', reg_type=[]):
    """Get specific Geography based on user id."""
    try:
        orgs = {}
        if registry == 'persons':
            geos = RegPersonsGeo.objects.select_related().filter(
                person_id__in=list_ids, is_void=False, date_delinked=None)
            # For getting all area ids for geo-locations
            for geo in geos:
                person_id = geo.person_id
                area_name = geo.area.area_name
                area_type = geo.area.area_type_id
                if area_type in reg_type:
                    if person_id not in orgs:
                        orgs[person_id] = [area_name]
                    else:
                        orgs[person_id].append(area_name)
        elif registry == 'person_orgs':
            geos = RegPersonsOrgUnits.objects.select_related().filter(
                person_id__in=list_ids, primary_unit=True,
                date_delinked=None, is_void=False)
            # For getting all geo ids for org units
            for geo in geos:
                person_id = geo.person_id
                org_name = geo.org_unit.org_unit_name
                if person_id not in orgs:
                    orgs[person_id] = [org_name]
                else:
                    orgs[person_id].append(org_name)
        elif registry == 'person_types':
            person_types = get_dict(field_name=['person_type_id'])
            geos = RegPersonsTypes.objects.select_related().filter(
                person_id__in=list_ids, is_void=False, date_ended=None)
            # For getting all person type ids for persons
            for geo in geos:
                person_id = geo.person_id
                type_id = geo.person_type_id
                if type_id in person_types:
                    type_name = person_types[type_id]
                    if person_id not in orgs:
                        orgs[person_id] = [type_name]
                    else:
                        orgs[person_id].append(type_name)
        else:
            geos = RegOrgUnitGeography.objects.select_related().filter(
                org_unit_id__in=list_ids, is_void=False, date_delinked=None)
            # For getting all area ids for geo-locations
            for geo in geos:
                org_id = geo.org_unit_id
                area_name = geo.area.area_name
                area_type = geo.area.area_type_id
                if area_type in reg_type:
                    if org_id not in orgs:
                        orgs[org_id] = [area_name]
                    else:
                        orgs[org_id].append(area_name)
    except Exception, e:
        error = 'Error getting geos - %s' % (str(e))
        print error
    else:
        return orgs


def get_specific_units(org_ids):
    """Get specific Organisational units based on lit of units."""
    try:
        result = RegOrgUnitGeography.objects.select_related().filter(
            org_unit_id__in=org_ids, is_void=False)
    except Exception, e:
        error = 'Error getting geos - %s' % (str(e))
        print error
    else:
        return result


def get_geo_selected(results, datas, extras, filters=False):
    """Get specific Geography based on existing ids."""
    wards = []
    all_list = get_all_geo_list(filters)
    results['wards'] = datas
    area_ids = map(int, datas)
    selected_ids = map(int, extras)
    # compare
    for geo_list in all_list:
        parent_area_id = geo_list['parent_area_id']
        area_id = geo_list['area_id']
        area_name = geo_list['area_name']
        if parent_area_id in area_ids:
            final_list = '%s,%s' % (area_id, area_name)
            wards.append(final_list)
        # attach already selected
        if area_id in selected_ids:
            extra_list = '%s,%s' % (area_id, area_name)
            wards.append(extra_list)
    unique_wards = list(set(wards))
    results['wards'] = unique_wards
    return results


def get_all_geo_list(filters=False):
    """Get all Geo Locations."""
    try:
        geo_lists = SetupGeography.objects.all()
        geo_lists = geo_lists.filter(is_void=False)
        if filters:
            all_geos = get_user_geos(filters)
            if all_geos:
                subcounty_list = list(all_geos['sub_counties'])
                all_ids = subcounty_list + list(all_geos['wards'])
                geo_lists = geo_lists.filter(area_id__in=all_ids)
        geo_lists = geo_lists.values(
            'area_id', 'area_type_id', 'area_name', 'parent_area_id')
        # .exclude(area_type_id='GPRV')
    except Exception, e:
        raise e
    else:
        return geo_lists


def get_geo_list(geo_lists, geo_filter, add_select=False, user_filter=[]):
    """Get specific Organisational units based on filter and list."""
    area_detail, result = {}, ()
    if add_select:
        area_detail[''] = 'Please Select'
    try:
        if geo_lists:
            for i, geo_list in enumerate(geo_lists):
                area_id = geo_list['area_id']
                area_name = geo_list['area_name']
                area_type = geo_list['area_type_id']
                if geo_filter == area_type:
                    if user_filter:
                        if area_id in user_filter:
                            area_detail[area_id] = area_name
                    else:
                        area_detail[area_id] = area_name
            result = area_detail.items()
    except Exception, e:
        raise e
    else:
        return result


def org_unit_type_filter(queryset, passed_in_org_types):
    """Get specific Organisational units based on a filter."""
    for passed_in_org_type in passed_in_org_types:
        queryset = queryset.filter(org_unit_type_id=passed_in_org_type)
    return queryset


def search_org_units(unit_types, is_closed):
    """Search function for all Organisational units - no filters."""
    try:
        org_units = RegOrgUnit.objects.all()
        org_units = org_units.filter(is_void=False)
        if not is_closed:
            org_units = org_units.filter(date_closed__isnull=True)
        if unit_types:
            # org_units = org_unit_type_filter(org_units, unit_types)
            org_units = org_units.filter(org_unit_type_id__in=unit_types)
    except Exception, e:
        error = "Error searching org units - %s" % (str(e))
        print error
        return {}
    else:
        return org_units


def get_all_org_units():
    """Get all Organisational units."""
    try:
        org_units = RegOrgUnit.objects.all().values(
            'id', 'org_unit_id_vis', 'org_unit_name')
    except Exception, e:
        error = "Error getting org units - %s" % (str(e))
        print error
        return None
    else:
        return org_units


def get_org_units(initial="Select unit"):
    """Get all Organisational units for drop down."""
    try:
        unit_detail = {'': initial} if initial else {}
        org_units = get_all_org_units()
        for unit in org_units:
            unit_vis = unit['org_unit_id_vis']
            unit_name = unit['org_unit_name']
            unit_detail[unit['id']] = '%s %s' % (unit_vis, unit_name)
    except Exception, e:
        print "error - %s" % (str(e))
        return {}
    else:
        return unit_detail.items()


def save_contacts(contact_id, contact_value, org_unit):
    """Save contacts for Organisational units."""
    try:
        contact, created = RegOrgUnitContact.objects.update_or_create(
            contact_detail_type_id=contact_id, org_unit_id=org_unit,
            defaults={'contact_detail_type_id': contact_id,
                      'contact_detail': contact_value,
                      'org_unit_id': org_unit, 'is_void': False},)
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return contact, created


def get_contacts(org_id):
    """Get specific Organisational units contacts from org id."""
    try:
        contact_dict = {}
        contacts = RegOrgUnitContact.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'contact_detail_type_id', 'contact_detail')
        for contact in contacts:
            contact_type = 'contact_%s' % (contact['contact_detail_type_id'])
            contact_dict[contact_type] = contact['contact_detail']
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return contact_dict


def save_external_ids(identifier_id, identifier_value, org_unit):
    """Save Organisational units external ids."""
    try:
        contact, created = RegOrgUnitExternalID.objects.update_or_create(
            identifier_type_id=identifier_id, org_unit_id=org_unit,
            defaults={'identifier_type_id': identifier_id,
                      'identifier_value': identifier_value,
                      'org_unit_id': org_unit, 'is_void': False},)
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return contact, created


def get_external_ids(org_id):
    """Get Organisational units ids for specific org id."""
    try:
        ext_ids = RegOrgUnitExternalID.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'identifier_type_id', 'identifier_value')
    except Exception, e:
        raise e
    else:
        return ext_ids


def perform_audit_persons(org_id):
    """TO DO."""
    try:
        ext_ids = RegOrgUnitExternalID.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'identifier_type_id', 'identifier_value')
    except Exception, e:
        raise e
    else:
        return ext_ids


def save_geo_location(area_ids, org_unit, existing_ids=[]):
    """Save Organisational units geo locations."""
    try:
        date_linked = datetime.now().strftime("%Y-%m-%d")
        # Delink those unselected by user
        area_ids = map(int, area_ids)
        delink_list = [x for x in existing_ids if x not in area_ids]
        for i, area_id in enumerate(area_ids):
            if area_id not in delink_list:
                geo, created = RegOrgUnitGeography.objects.update_or_create(
                    area_id=area_id, org_unit_id=org_unit,
                    defaults={'date_linked': date_linked, 'is_void': False},)
        if delink_list:
            for i, area_id in enumerate(delink_list):
                geo, created = RegOrgUnitGeography.objects.update_or_create(
                    area_id=area_id, org_unit_id=org_unit,
                    defaults={'date_delinked': date_linked, 'is_void': True},)
    except Exception, e:
        error = 'Error linking area to org unit -%s' % (str(e))
        print error
        return None
    else:
        return True


def get_geo_location(org_id):
    """Get specific Organisational units location based on org id."""
    try:
        ext_ids = RegOrgUnitGeography.objects.filter(
            org_unit_id=org_id, is_void=False).values('area_id')
    except Exception, e:
        raise e
    else:
        return ext_ids


def close_org_unit(close_date, org_unit_id):
    """Close Organisational units based on org id."""
    try:
        if not close_date:
            close_date = datetime.now().strftime("%Y-%m-%d")
        org_unit = get_object_or_404(RegOrgUnit, pk=org_unit_id)
        org_unit.date_closed = close_date
        org_unit.save(update_fields=["date_closed"])
    except Exception, e:
        raise e
    else:
        pass


def set_person_dead(date_of_death, person_id):
    """Mark person as dead based on person id."""
    try:
        if not date_of_death:
            date_of_death = datetime.now().strftime("%Y-%m-%d")
        person_detail = get_object_or_404(RegPerson, pk=person_id)
        person_detail.date_of_death = date_of_death
        person_detail.save(update_fields=["date_of_death"])
    except Exception, e:
        raise e


def delete_org_unit(org_unit_id):
    """Mark as void an Organisational unit."""
    try:
        org_unit = get_object_or_404(RegOrgUnit, pk=org_unit_id)
        org_unit.is_void = True
        org_unit.save(update_fields=["is_void"])
    except Exception, e:
        raise e


def delete_person(person_id):
    """Mark as void a person."""
    try:
        person_detail = get_object_or_404(RegPerson, pk=person_id)
        person_detail.is_void = True
        person_detail.save(update_fields=["is_void"])
    except Exception, e:
        raise e


def new_guid_32():
    """Method to generate guid with dashes removed."""
    return str(uuid.uuid1()).replace('-', '')


def org_id_generator(modelid):
    """Method for generating org unit id."""
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return organisation_id_prefix + str(uniqueid) + str(checkdigit)


def luhn_checksum(check_number):
    """http://en.wikipedia.org/wiki/Luhn_algorithm ."""
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(check_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10


def is_luhn_valid(check_number):
    """http://en.wikipedia.org/wiki/Luhn_algorithm ."""
    return luhn_checksum(check_number) == 0


def calculate_luhn(partial_check_number):
    """http://en.wikipedia.org/wiki/Luhn_algorithm ."""
    check_digit = luhn_checksum(int(partial_check_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit


def get_client_ip(request):
    """Get IP address for both ajax and normal requests."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_meta_data(request):
    """Method to get meta data."""
    try:
        meta_info = {}
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        meta_info['browser'] = user_agent
        # Compress this text
        content = json.dumps(meta_info, separators=(',', ':'))
        return str(content)
    except Exception:
        return None
