from .models import CPOVCRole, CPOVCUserRoleGeoOrg


def get_allowed_units_county(user_id):
    '''
    Return dict with list of allowed group ids mapped to org units
    and for sub counties do the reverse just list of sub-counties
    '''
    try:
        geo_orgs = get_group_geos_org(user_id)
        ex_areas, ex_orgs = [], {}
        for geo_org in geo_orgs:
            if geo_org['area_id']:
                ex_areas.append(geo_org['area_id'])
            if geo_org['org_unit_id']:
                if geo_org['org_unit_id'] in ex_orgs:
                    ex_orgs[geo_org['org_unit_id']].append(geo_org['group_id'])
                else:
                    ex_orgs[geo_org['org_unit_id']] = [geo_org['group_id']]
    except Exception, e:
        error = 'Error getting persons orgs/sub-county groups - %s' % (str(e))
        print error
    else:
        return ex_areas, ex_orgs


def get_groups(grp_prefix='group_'):
    '''
    Return list of ids and CPIMS codes
    '''
    groups = {}
    try:
        results = CPOVCRole.objects.filter().values(
            'group_ptr_id', 'group_id', 'group_name')
        for group in results:
            group_id = '%s%s' % (grp_prefix, str(group['group_id']))
            groups[group['group_ptr_id']] = group_id

    except Exception, e:
        error = 'Error getting groups - %s' % (str(e))
        print error
    else:
        return groups


def get_group_geos_org(user_id):
    try:
        result = CPOVCUserRoleGeoOrg.objects.filter(
            user_id=user_id, is_void=False).values(
                'area_id', 'group_id', 'org_unit_id')
    except Exception, e:
        error = 'Error getting geo/orgs by groups - %s' % (str(e))
        print error
    else:
        return result


def remove_group_geo_org(user_id, group_id, area_id, org_unit_id):
    try:
        geo_orgs = CPOVCUserRoleGeoOrg.objects.get(
            user_id=user_id, group_id=group_id, is_void=False,
            area_id=area_id, org_unit_id=org_unit_id)
        geo_orgs.is_void = True
        geo_orgs.save(update_fields=['is_void'])
    except Exception, e:
        error = 'Error removing org unit -%s' % (str(e))
        print error
        return None
    else:
        return geo_orgs


def save_group_geo_org(user_id, group_id, area_id, org_unit_id):
    try:
        geo_org_perm, created = CPOVCUserRoleGeoOrg.objects.update_or_create(
            user_id=user_id, group_id=group_id, is_void=False,
            defaults={'area_id': area_id, 'org_unit_id': org_unit_id,
                      'is_void': False},)
    except Exception, e:
        error = 'Error searching org unit -%s' % (str(e))
        print error
        return None
    else:
        return geo_org_perm, created
