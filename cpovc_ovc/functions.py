"""OVC common methods."""
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import connection
from .models import (
    OVCRegistration, OVCHouseHold, OVCHHMembers, OVCHealth, OVCEligibility,
    OVCFacility, OVCSchool, OVCEducation)
from cpovc_registry.models import RegPerson, RegOrgUnit, RegPersonsTypes
from cpovc_main.functions import convert_date
from cpovc_registry.functions import extract_post_params, save_person_extids


def search_ovc(name, criteria):
    """Method to search OVC as per USG."""
    try:
        cid = int(criteria)
        cbos, pids, chvs = [], [], []
        designs = ['COVC', 'CGOC']
        if cid in [2, 3, 4]:
            queryset = None
        else:
            queryset = RegPerson.objects.filter(
                is_void=False, designation__in=designs)
        field_names = ['surname', 'first_name', 'other_names']
        q_filter = Q()
        # 1: Names, 2: HH, 3: CHV, 4: CBO
        names = name.split()
        if cid == 0:
            for nm in names:
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: name})
                pids = queryset.filter(q_filter).values_list(
                    'id', flat=True)
        elif cid == 1:
            pids = []
            query = ("SELECT id FROM reg_person WHERE to_tsvector"
                     "(first_name || ' ' || surname || ' ' || other_names)"
                     " @@ to_tsquery('%s') ORDER BY date_of_birth DESC")
            # " OFFSET 10 LIMIT 10")
            vals = ' & '.join(names)
            sql = query % (vals)
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchall()
                print row
                pids = [r[0] for r in row]
                print 'pppp', pids
        elif cid == 2:
            pids = OVCHHMembers.objects.filter(
                is_void=False,
                house_hold__head_identifier__iexact=name).values_list(
                'person_id', flat=True)
        elif cid == 3:
            chv_ids = RegPersonsTypes.objects.filter(
                is_void=False, person_type_id='TWVL').values_list(
                'person_id', flat=True)
            queryset = RegPerson.objects.filter(
                is_void=False, id__in=chv_ids)
            for nm in names:
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: nm})
            chvs = queryset.filter(q_filter).values_list(
                'id', flat=True)
        elif cid == 4:
            cbos = RegOrgUnit.objects.filter(
                is_void=False, org_unit_name__icontains=name).values_list(
                'id', flat=True)
        else:
            for nm in names:
                for field in field_names:
                    q_filter |= Q(**{"%s__icontains" % field: name})
                pids = queryset.filter(q_filter).values_list(
                    'id', flat=True)
        # Query ovc table
        qs = OVCRegistration.objects.filter(is_void=False)
        pst, plen = 0, 100
        if cbos:
            ovcs = qs.filter(child_cbo_id__in=cbos)[pst:plen]
        elif chvs:
            ovcs = qs.filter(child_chv_id__in=chvs)[pst:plen]
        else:
            ovcs = qs.filter(person_id__in=pids)[pst:plen]
    except Exception, e:
        print 'Error searching for OVC - %s' % (str(e))
        return {}
    else:
        return ovcs


def search_master(request):
    """Method to query existing customers."""
    try:
        results = []
        query_id = int(request.GET.get('id'))
        query = request.GET.get('q')
        # Filters for external ids
        if query_id == 1:
            agents = OVCFacility.objects.filter(
                facility_name__icontains=query)
            for agent in agents:
                name = agent.facility_name
                agent_id = agent.id
                val = {'id': agent_id, 'label': name,
                       'value': name}
                results.append(val)
        elif query_id == 2:
            agents = OVCSchool.objects.filter(
                school_name__icontains=query)
            for agent in agents:
                name = agent.school_name
                agent_id = agent.id
                val = {'id': agent_id, 'label': name,
                       'value': name}
                results.append(val)
    except Exception, e:
        print 'error searching master list - %s' % (str(e))
        return []
    else:
        return results


def get_hh_members(ovc_id):
    """Method to get child chv details."""
    try:
        ovc_detail = get_object_or_404(
            OVCHHMembers, person_id=ovc_id, is_void=False)
    except Exception, e:
        print 'error getting ovc hh members - %s' % (str(e))
        return {}
    else:
        return ovc_detail


def get_ovcdetails(ovc_id):
    """Method to get child chv details."""
    try:
        ovc_detail = get_object_or_404(
            OVCRegistration, person_id=ovc_id, is_void=False)
    except Exception, e:
        print 'error getting ovc details - %s' % (str(e))
        return {}
    else:
        return ovc_detail


def ovc_registration(request, ovc_id, edit=0):
    """Method to complete ovc registration."""
    try:
        reg_date = request.POST.get('reg_date')
        bcert = request.POST.get('has_bcert')
        disabled = request.POST.get('disb')
        hh_members = request.POST.getlist('hh_member')
        cbo_id = request.POST.get('cbo_id')
        has_bcert = True if bcert else False
        is_disabled = True if disabled else False

        bcert_no = request.POST.get('bcert_no')
        ncpwd_no = request.POST.get('ncpwd_no')
        ext_ids = {}
        if bcert_no:
            ext_ids['ISOV'] = bcert_no
        if ncpwd_no:
            ext_ids['IPWD'] = ncpwd_no
        if ext_ids:
            save_person_extids(ext_ids, ovc_id)

        hiv_status = request.POST.get('hiv_status')
        immmune = request.POST.get('immunization')
        org_uid = request.POST.get('cbo_uid')
        org_uid_check = request.POST.get('cbo_uid_check')
        caretaker = request.POST.get('caretaker')
        school_level = request.POST.get('school_level')
        is_exited = request.POST.get('is_exited')
        exit_reason = request.POST.get('exit_reason')
        criterias = request.POST.getlist('eligibility')
        reg_date = datetime.now().strftime("%Y-%m-%d")
        if edit == 0:
            cbo_uid = gen_cbo_id(cbo_id, ovc_id)
            org_cid = cbo_uid if org_uid == org_uid_check else org_uid
        else:
            org_cid = org_uid
        is_active = False if is_exited else True
        ovc_detail = get_object_or_404(OVCRegistration, person_id=ovc_id)
        ovc_detail.registration_date = reg_date
        ovc_detail.has_bcert = has_bcert
        ovc_detail.is_disabled = is_disabled
        ovc_detail.hiv_status = str(hiv_status)
        ovc_detail.immunization_status = str(immmune)
        ovc_detail.org_unique_id = org_cid
        ovc_detail.caretaker_id = caretaker
        ovc_detail.school_level = school_level
        ovc_detail.is_active = is_active
        ovc_detail.exit_reason = exit_reason
        ovc_detail.save(
            update_fields=["registration_date", "has_bcert", "is_disabled",
                           "hiv_status", "immunization_status",
                           "org_unique_id", "caretaker_id", "school_level",
                           "is_active", "exit_reason"])
        # Update eligibility
        for criteria_id in criterias:
            eligibility, created = OVCEligibility.objects.update_or_create(
                person_id=ovc_id, criteria=criteria_id,
                defaults={'person_id': ovc_id, 'criteria': criteria_id},)
        # Update Health status
        if hiv_status == 'HSTP':
            facility = request.POST.get('facility_id')
            art_status = request.POST.get('art_status')
            link_date = request.POST.get('link_date')
            date_linked = convert_date(link_date)
            ccc_no = request.POST.get('ccc_number')
            health, created = OVCHealth.objects.update_or_create(
                person_id=ovc_id,
                defaults={'person_id': ovc_id,
                          'facility_id': facility, 'art_status': art_status,
                          'date_linked': date_linked, 'ccc_number': ccc_no,
                          'is_void': False},)
        # Update School details
        if school_level != 'SLNS':
            school_class = request.POST.get('school_class')
            school_id = request.POST.get('school_id')
            school_adm = request.POST.get('admission_type')
            health, created = OVCEducation.objects.update_or_create(
                person_id=ovc_id, school_class=school_class,
                defaults={'person_id': ovc_id,
                          'school_id': school_id, 'school_level': school_level,
                          'school_class': school_class,
                          'admission_type': school_adm,
                          'is_void': False},)
        cgs = extract_post_params(request, naming='cg_')
        hhrs = extract_post_params(request, naming='hhr_')
        # Alive status, HIV status and Death cause
        ast = extract_post_params(request, naming='astatus_')
        hst = extract_post_params(request, naming='gstatus_')
        cst = extract_post_params(request, naming='cstatus_')
        todate = timezone.now()
        if edit == 0:
            # Create House Hold and populate members
            caretaker_id = int(cgs[caretaker][0])
            new_hh = OVCHouseHold(
                head_person_id=caretaker,
                head_identifier=caretaker_id)
            new_hh.save()
            hh_id = new_hh.pk
            # Add members to HH
            hh_members.append(ovc_id)
            for hh_member in hh_members:
                oid = int(ovc_id)
                hh_head = True if int(hh_member) == caretaker_id else False
                hh_hiv = hst[hh_member][0] if hh_member in hst else None
                hh_alive = ast[hh_member][0] if hh_member in ast else 'AYES'
                hh_death = cst[hh_member][0] if hh_member in cst else None
                m_type = hhrs[hh_member][0] if hh_member in hhrs else 'TBVC'
                member_type = 'TOVC' if oid == int(hh_member) else m_type
                print 'hh_death', hh_death
                OVCHHMembers(
                    house_hold_id=hh_id, person_id=hh_member,
                    hh_head=hh_head, member_type=member_type,
                    death_cause=hh_death, member_alive=hh_alive,
                    hiv_status=hh_hiv, date_linked=todate).save()
        else:
            # Update HH details
            hhid = request.POST.get('hh_id')
            caretaker_id = cgs[caretaker][0]
            hh_detail = get_object_or_404(OVCHouseHold, id=hhid)
            hh_detail.head_person_id = caretaker
            hh_detail.head_identifier = caretaker_id
            hh_detail.save(update_fields=["head_identifier", "head_person"])
            # Update HH Members
            for hh_member in hhrs:
                hh_hiv = hst[hh_member][0] if hh_member in hst else None
                hh_head = True if hh_member == caretaker else False
                hh_alive = ast[hh_member][0] if hh_member in ast else 'AYES'
                hh_death = cst[hh_member][0] if hh_member in cst else None
                member_type = hhrs[hh_member][0]
                hhm, created = OVCHHMembers.objects.update_or_create(
                    person_id=hh_member, house_hold_id=hhid,
                    defaults={'person_id': hh_member, 'hh_head': hh_head,
                              'member_type': member_type, 'is_void': False,
                              'death_cause': hh_death,
                              'member_alive': hh_alive,
                              'date_linked': todate, 'hiv_status': hh_hiv},)
    except Exception, e:
        raise e
    else:
        pass


def gen_cbo_id(cbo_id, ovc_id):
    """Invoice validations."""
    try:
        last_id = OVCRegistration.objects.filter(
            child_cbo_id=cbo_id).exclude(org_unique_id__isnull=True).order_by(
                'org_unique_id').last()
        if not last_id:
            return '00001'
        lid = last_id.org_unique_id
        if lid and lid.isnumeric():
            new_id = str(int(lid) + 1).zfill(5)
        else:
            if lid:
                new_id = '%sX' % (lid[:-1])
            else:
                '0000X'
        return new_id
    except Exception, e:
        raise e
    else:
        pass
