import uuid
from datetime import datetime
from django.shortcuts import get_object_or_404
from cpovc_main.models import SetupGeography
from .models import (
    RegOrgUnitContact, RegOrgUnit, RegOrgUnitExternalID, RegOrgUnitGeography)

organisation_id_prefix = 'U'
benficiary_id_prefix = 'B'
workforce_id_prefix = 'W'


def get_all_geo_list():
    try:
        geo_lists = SetupGeography.objects.all().values(
            'area_id', 'area_type_id', 'area_name', 'parent_area_id')
        # .exclude(area_type_id='GPRV')
    except Exception, e:
        raise e
    else:
        return geo_lists


def get_geo_list(geo_lists, geo_filter):
    # [{'area_id': 48, 'area_name': u'Changamwe', 'area_type_id': u'GDIS'}
    area_detail, result = {}, ()
    area_detail[''] = 'Please Select'
    try:
        if geo_lists:
            for i, geo_list in enumerate(geo_lists):
                area_id = geo_list['area_id']
                area_name = geo_list['area_name']
                area_type = geo_list['area_type_id']
                if geo_filter == area_type:
                    area_detail[area_id] = area_name
            result = area_detail.items()
    except Exception, e:
        raise e
    else:
        return result


def get_all_org_units():
    try:
        org_units = RegOrgUnit.objects.all().values(
            'id', 'org_unit_id_vis', 'org_unit_name')
    except Exception, e:
        error = "Error getting org units - %s" % (str(e))
        print error
        return None
    else:
        return org_units


def get_org_units():
    try:
        unit_detail = {}
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
    try:
        ext_ids = RegOrgUnitExternalID.objects.filter(
            org_unit_id=org_id, is_void=False).values(
            'identifier_type_id', 'identifier_value')
    except Exception, e:
        raise e
    else:
        return ext_ids


def save_geo_location(area_ids, org_unit, existing_ids=[]):
    try:
        date_linked = datetime.now().strftime("%Y-%m-%d")
        # Delink those unselected by user
        area_ids = map(int, area_ids)
        print area_ids
        print '--' * 40
        print existing_ids
        delink_list = [x for x in existing_ids if x not in area_ids]
        print '--' * 40
        print delink_list
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
    try:
        ext_ids = RegOrgUnitGeography.objects.filter(
            org_unit_id=org_id, is_void=False).values('area_id')
    except Exception, e:
        raise e
    else:
        return ext_ids


def close_org_unit(close_date, org_unit_id):
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


def new_guid_32():
    return str(uuid.uuid1()).replace('-', '')


def org_id_generator(modelid):
    uniqueid = '%05d' % modelid
    checkdigit = calculate_luhn(str(uniqueid))
    return organisation_id_prefix + str(uniqueid) + str(checkdigit)


def luhn_checksum(check_number):
    '''
    http://en.wikipedia.org/wiki/Luhn_algorithm
    '''
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
    '''
    http://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    return luhn_checksum(check_number) == 0


def calculate_luhn(partial_check_number):
    '''
    http://en.wikipedia.org/wiki/Luhn_algorithm
    '''
    check_digit = luhn_checksum(int(partial_check_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit
