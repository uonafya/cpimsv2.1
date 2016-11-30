"""OVC Care views."""
from django.shortcuts import render
from .forms import OVCSearchForm, OVCRegistrationForm
from django.db.models import Q
from cpovc_registry.models import (
    RegPerson, RegPersonsGuardians, RegPersonsSiblings, RegPersonsExternalIds)
from cpovc_main.functions import get_dict
from .models import OVCRegistration, OVCHHMembers, OVCHealth
from .functions import ovc_registration


def ovc_home(request):
    """Some default page for Server Errors."""
    try:
        if request.method == 'POST':
            form = OVCSearchForm(data=request.POST)
            query = request.POST.get('search_name')

            designs = ['COVC', 'CGOC']

            queryset = RegPerson.objects.filter(
                is_void=False, designation__in=designs)
            field_names = ['surname', 'first_name', 'other_names']
            q_filter = Q()
            for field in field_names:
                q_filter |= Q(**{"%s__icontains" % field: query})
            persons = queryset.filter(q_filter)
            # Query ovc table
            pids = []
            for person in persons:
                pids.append(person.id)
            ovcs = OVCRegistration.objects.filter(
                is_void=False, person_id__in=pids)

            return render(request, 'ovc/home.html',
                          {'form': form, 'persons': persons, 'ovcs': ovcs})
        form = OVCSearchForm()
        return render(request, 'ovc/home.html', {'form': form, 'status': 200})
    except Exception, e:
        raise e


def ovc_register(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        if request.method == 'POST':
            form = OVCRegistrationForm(data=request.POST)
            print request.POST
            ovc_registration(request, ovc_id)
        else:
            form = OVCRegistrationForm()
        child = RegPerson.objects.get(is_void=False, id=id)
        params = {}
        gparams = {}
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        guids = []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        # Re-usable values
        check_fields = ['relationship_type_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/register_child.html',
                      {'form': form, 'status': 200, 'child': child,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'extids': gparams})
    except Exception, e:
        print "error with OVC registration - %s" % (str(e))
        raise e


def ovc_edit(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        date_reg = None
        if request.method == 'POST':
            form = OVCRegistrationForm(data=request.POST)
            ovc_registration(request, ovc_id, 1)
            # Save external ids from here
        child = RegPerson.objects.get(is_void=False, id=ovc_id)
        creg = OVCRegistration.objects.get(is_void=False, person_id=ovc_id)
        bcert = 'on' if creg.has_bcert else ''
        disb = 'on' if creg.is_disabled else ''
        reg_date = creg.registration_date
        child.caretaker = creg.caretaker_id
        child.cbo = creg.child_cbo.org_unit_name
        child.chv_name = creg.child_chv.full_name
        params = {}
        gparams = {}
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        guids = []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        # Get health information
        ccc_no, date_linked, art_status, facility = '', '', '', ''
        if creg.hiv_status == 'HSTP':
            health = OVCHealth.objects.get(person_id=ovc_id)
            ccc_no = health.ccc_number
            date_linked = health.date_linked.strftime('%d-%b-%Y')
            art_status = health.art_status
            facility = health.facility_id
        bcert_no = params['ISOV'] if 'ISOV' in params else ''
        ncpwd_no = params['IPWD'] if 'IPWD' in params else ''
        if reg_date:
            date_reg = reg_date.strftime('%d-%b-%Y')
        all_values = {'reg_date': date_reg, 'cbo_uid': creg.org_unique_id,
                      'has_bcert': bcert, 'disb': disb,
                      'bcert_no': bcert_no, 'ncpwd_no': ncpwd_no,
                      'immunization': creg.immunization_status,
                      'school_level': creg.school_level, 'facility': facility,
                      'hiv_status': creg.hiv_status, 'link_date': date_linked,
                      'ccc_number': ccc_no, 'art_status': art_status}
        form = OVCRegistrationForm(data=all_values)

        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        # Get house hold
        hhold = OVCHHMembers.objects.get(
            is_void=False, person_id=child.id)
        # Re-usable values
        check_fields = ['relationship_type_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/edit_child.html',
                      {'form': form, 'status': 200, 'child': child,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'hhold': hhold, 'extids': gparams})
    except Exception, e:
        print "error with OVC editing - %s" % (str(e))
        raise e


def ovc_view(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        child = RegPerson.objects.get(is_void=False, id=ovc_id)
        creg = OVCRegistration.objects.get(is_void=False, person_id=ovc_id)
        params = {}
        gparams = {}
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        guids = []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        # Health details
        health = {}
        if creg.hiv_status == 'HSTP':
            health = OVCHealth.objects.get(person_id=ovc_id)
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        # Get house hold
        hhold = OVCHHMembers.objects.get(
            is_void=False, person_id=child.id)
        # Re-usable values
        check_fields = ['relationship_type_id', 'school_level_id',
                        'hiv_status_id', 'immunization_status_id',
                        'art_status_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/view_child.html',
                      {'status': 200, 'child': child, 'params': params,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'hhold': hhold, 'creg': creg,
                       'extids': gparams, 'health': health})
    except Exception, e:
        print "error with OVC viewing - %s" % (str(e))
        raise e


def hh_manage(request, hhid):
    """Some default page for Server Errors."""
    try:
        hhmembers = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        return render(request, 'ovc/household.html',
                      {'status': 200, 'hhmembers': hhmembers})
    except Exception, e:
        print "error getting hh members - %s" % (str(e))
        raise e
