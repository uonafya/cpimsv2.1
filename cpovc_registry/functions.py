import uuid
from .models import RegOrgUnitContact, RegOrgUnit, RegOrgUnitExternalID

organisation_id_prefix = 'U'
benficiary_id_prefix = 'B'
workforce_id_prefix = 'W'


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
        print unit_detail
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
