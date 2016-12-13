"""OVC common methods."""
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import (
    OVCRegistration, OVCHouseHold, OVCHHMembers, OVCHealth)
from cpovc_main.functions import convert_date
from cpovc_registry.functions import extract_post_params, save_person_extids


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

        print request.POST

        hiv_status = request.POST.get('hiv_status')
        immmune = request.POST.get('immunization')
        org_uid = request.POST.get('cbo_uid')
        caretaker = request.POST.get('caretaker')
        school_level = request.POST.get('school_level')
        reg_date = datetime.now().strftime("%Y-%m-%d")
        ovc_detail = get_object_or_404(OVCRegistration, person_id=ovc_id)
        ovc_detail.registration_date = reg_date
        ovc_detail.has_bcert = has_bcert
        ovc_detail.is_disabled = is_disabled
        ovc_detail.hiv_status = str(hiv_status)
        ovc_detail.immunization_status = str(immmune)
        ovc_detail.org_unique_id = org_uid
        ovc_detail.caretaker_id = caretaker
        ovc_detail.school_level = school_level
        ovc_detail.save(
            update_fields=["registration_date", "has_bcert", "is_disabled",
                           "hiv_status", "immunization_status",
                           "org_unique_id", "caretaker_id", "school_level"])
        # Update Health status
        if hiv_status == 'HSTP':
            facility = request.POST.get('facility')
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
        cgs = extract_post_params(request, naming='cg_')
        hhrs = extract_post_params(request, naming='hhr_')
        todate = timezone.now()
        if edit == 0:
            # Create House Hold and populate members
            caretaker_id = cgs[caretaker][0]
            new_hh = OVCHouseHold(
                head_person_id=caretaker,
                head_identifier=caretaker_id)
            new_hh.save()
            hh_id = new_hh.pk
            # Add members to HH
            hh_members.append(ovc_id)
            for hh_member in hh_members:
                hh_head = True if hh_member == caretaker_id else False
                m_type = hhrs[hh_member][0] if hh_member in hhrs else 'TBVC'
                OVCHHMembers(
                    house_hold_id=hh_id, person_id=hh_member,
                    hh_head=hh_head, member_type=m_type,
                    date_linked=todate).save()
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
                print hh_member
                hh_head = True if hh_member == caretaker else False
                member_type = hhrs[hh_member][0]
                hhm, created = OVCHHMembers.objects.update_or_create(
                    person_id=hh_member, house_hold_id=hhid,
                    defaults={'person_id': hh_member, 'hh_head': hh_head,
                              'member_type': member_type, 'is_void': False,
                              'date_linked': todate},)
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
