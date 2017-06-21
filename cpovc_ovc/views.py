"""OVC Care views."""
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import OVCSearchForm, OVCRegistrationForm
from cpovc_registry.models import (
    RegPerson, RegPersonsGuardians, RegPersonsSiblings, RegPersonsExternalIds)
from cpovc_main.functions import get_dict
from .models import OVCRegistration, OVCHHMembers, OVCHealth, OVCEligibility
from .functions import (
    ovc_registration, get_hh_members, get_ovcdetails, gen_cbo_id, search_ovc,
    search_master)


@login_required(login_url='/')
def ovc_home(request):
    """Some default page for Server Errors."""
    try:
        if request.method == 'POST':
            form = OVCSearchForm(data=request.POST)
            query = request.POST.get('search_name')
            criteria = request.POST.get('search_criteria')

            ovcs = search_ovc(query, criteria)

            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)

            return render(request, 'ovc/home.html',
                          {'form': form, 'ovcs': ovcs,
                           'vals': vals})
        form = OVCSearchForm()
        return render(request, 'ovc/home.html', {'form': form, 'status': 200})
    except Exception, e:
        raise e


def ovc_search(request):
    """Method to do ovc search."""
    try:
        results = search_master(request)
    except Exception, e:
        print 'error with search - %s' % (str(e))
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    else:
        return JsonResponse(results, content_type='application/json',
                            safe=False)


@login_required(login_url='/')
def ovc_register(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        ovc = get_ovcdetails(ovc_id)
        params, gparams = {}, {}
        initial = {}
        # Details
        child = RegPerson.objects.get(is_void=False, id=id)
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        print 'p', params, 'gp', gparams
        guids, chids = [], []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        for sibling in siblings:
            chids.append(sibling.sibling_person_id)
        pids = {'guids': guids, 'chids': chids}
        print pids
        # Existing
        extids = RegPersonsExternalIds.objects.filter(
            person_id__in=guids)
        for extid in extids:
            if extid.person_id == child.id:
                params[extid.identifier_type_id] = extid.identifier
            else:
                gkey = '%s_%s' % (extid.person_id, extid.identifier_type_id)
                gparams[gkey] = extid.identifier
        if request.method == 'POST':
            form = OVCRegistrationForm(guids=pids, data=request.POST)
            print request.POST
            ovc_registration(request, ovc_id)
            msg = "OVC Registration completed successfully"
            messages.info(request, msg)
            url = reverse('ovc_view', kwargs={'id': ovc_id})
            return HttpResponseRedirect(url)
        else:
            cbo_id = ovc.child_cbo_id
            cbo_uid = gen_cbo_id(cbo_id, ovc_id)
            initial['cbo_uid'] = cbo_uid
            initial['cbo_uid_check'] = cbo_uid
            if 'ISOV' in params:
                initial['bcert_no'] = params['ISOV']
                initial['has_bcert'] = 'on'
            form = OVCRegistrationForm(
                guids=pids, initial=initial)
        # Check users changing ids in urls
        ovc_detail = get_hh_members(ovc_id)
        if ovc_detail:
            msg = "OVC already registered. Visit edit page."
            messages.error(request, msg)
            url = reverse('ovc_view', kwargs={'id': ovc_id})
            return HttpResponseRedirect(url)
        # Re-usable values
        check_fields = ['relationship_type_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/register_child.html',
                      {'form': form, 'status': 200, 'child': child,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'extids': gparams, 'ovc': ovc})
    except Exception, e:
        print "error with OVC registration - %s" % (str(e))
        raise e


@login_required(login_url='/')
def ovc_edit(request, id):
    """Some default page for Server Errors."""
    try:
        ovc_id = int(id)
        date_reg = None
        if request.method == 'POST':
            ovc_registration(request, ovc_id, 1)
            # Save external ids from here
            msg = "OVC Registration details edited successfully"
            messages.info(request, msg)
            url = reverse('ovc_view', kwargs={'id': ovc_id})
            return HttpResponseRedirect(url)
        child = RegPerson.objects.get(is_void=False, id=ovc_id)
        creg = OVCRegistration.objects.get(is_void=False, person_id=ovc_id)
        bcert = 'on' if creg.has_bcert else ''
        disb = 'on' if creg.is_disabled else ''
        exited = '' if creg.is_active else 'on'
        reg_date = creg.registration_date
        child.caretaker = creg.caretaker_id
        child.cbo = creg.child_cbo.org_unit_name
        child.chv_name = creg.child_chv.full_name
        params = {}
        gparams = {}
        # Get guardians
        guardians = RegPersonsGuardians.objects.filter(
            is_void=False, child_person_id=child.id)
        # Get siblings
        siblings = RegPersonsSiblings.objects.filter(
            is_void=False, child_person_id=child.id)
        print 'p', params, 'gp', gparams
        guids, chids = [], []
        for guardian in guardians:
            guids.append(guardian.guardian_person_id)
        guids.append(child.id)
        for sibling in siblings:
            chids.append(sibling.sibling_person_id)
        pids = {'guids': guids, 'chids': chids}
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
        # Eligibility
        criterias = OVCEligibility.objects.filter(
            is_void=False, person_id=child.id).values_list(
            'criteria', flat=True)
        if reg_date:
            date_reg = reg_date.strftime('%d-%b-%Y')
        all_values = {'reg_date': date_reg, 'cbo_uid': creg.org_unique_id,
                      'cbo_uid_check': creg.org_unique_id,
                      'has_bcert': bcert, 'disb': disb,
                      'bcert_no': bcert_no, 'ncpwd_no': ncpwd_no,
                      'immunization': creg.immunization_status,
                      'school_level': creg.school_level, 'facility': facility,
                      'hiv_status': creg.hiv_status, 'link_date': date_linked,
                      'ccc_number': ccc_no, 'art_status': art_status,
                      'eligibility': criterias, 'is_exited': exited,
                      'exit_reason': creg.exit_reason}
        form = OVCRegistrationForm(guids=pids, data=all_values)
        # Get house hold
        hhold = OVCHHMembers.objects.get(
            is_void=False, person_id=child.id)
        hhid = hhold.house_hold_id
        hhmembers = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        # add caregivers hiv status
        for hhm in hhmembers:
            status_id = 'gstatus_%s' % (hhm.person_id)
            all_values[status_id] = hhm.hiv_status
        # Class levels
        levels = {}
        levels["SLNS"] = []
        levels["AECD"] = ["BABY,Baby Class", "MIDC,Middle Class",
                          "PREU,Pre-Unit"]
        levels["ACPR"] = ["CLS1,Class 1", "CLS2,Class 2", "CLS3,Class 3",
                          "CLS4,Class 4", "CLS5,Class 5", "CLS6,Class 6",
                          "CLS7,Class 7", "CLS8,Class 8"]
        levels["ACSC"] = ["FOM1,Form 1", "FOM2,Form 2", "FOM3,Form 3",
                          "FOM4,Form 4", "FOM5,Form 5", "FOM6,Form 6"]
        levels["ACVT"] = ["YER1,Year 1", "YER2,Year 2", "YER3,Year 3",
                          "YER4,Year 4", "YER5,Year 5", "YER6,Year 6"]
        levels["AUNV"] = ["TVC1,Year 1", "TVC2,Year 2", "TVC3,Year 3",
                          "TVC4,Year 4", "TVC5,Year 5"]
        # Re-usable values
        check_fields = ['relationship_type_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/edit_child.html',
                      {'form': form, 'status': 200, 'child': child,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'hhold': hhold, 'extids': gparams,
                       'hhmembers': hhmembers, 'levels': levels})
    except Exception, e:
        print "error with OVC editing - %s" % (str(e))
        raise e


@login_required(login_url='/')
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
        # Get HH members
        hhid = hhold.house_hold_id
        hhmqs = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        hhmembers = hhmqs.exclude(person_id=child.id)
        # Re-usable values
        check_fields = ['relationship_type_id', 'school_level_id',
                        'hiv_status_id', 'immunization_status_id',
                        'art_status_id']
        vals = get_dict(field_name=check_fields)
        return render(request, 'ovc/view_child.html',
                      {'status': 200, 'child': child, 'params': params,
                       'guardians': guardians, 'siblings': siblings,
                       'vals': vals, 'hhold': hhold, 'creg': creg,
                       'extids': gparams, 'health': health,
                       'hhmembers': hhmembers})
    except Exception, e:
        print "error with OVC viewing - %s" % (str(e))
        raise e


@login_required(login_url='/')
def hh_manage(request, hhid):
    """Some default page for Server Errors."""
    try:
        check_fields = ['hiv_status_id', 'immunization_status_id']
        vals = get_dict(field_name=check_fields)
        hhmembers = OVCHHMembers.objects.filter(
            is_void=False, house_hold_id=hhid).order_by("-hh_head")
        return render(request, 'ovc/household.html',
                      {'status': 200, 'hhmembers': hhmembers,
                       'vals': vals})
    except Exception, e:
        print "error getting hh members - %s" % (str(e))
        raise e
