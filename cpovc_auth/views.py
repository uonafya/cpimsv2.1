from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from cpovc_auth.forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import formset_factory

from .functions import (
    save_group_geo_org, remove_group_geo_org, get_allowed_units_county,
    get_groups)
from .models import AppUser
from cpovc_registry.models import (
    RegPerson, RegPersonsExternalIds, RegPersonsOrgUnits, RegPersonsGeo)

from .forms import RolesOrgUnits, RolesGeoArea, RolesForm
from .decorators import is_allowed_groups


def home(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'base.html', {'status': 200})
    except Exception, e:
        raise e


def log_in(request):
    '''
    Method to handle log in to system
    '''
    try:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.data['username'].strip()
                password = form.data['password'].strip()
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # grps = user.groups.all()
                        return HttpResponseRedirect(reverse(home))
                    else:
                        msg = "Login Account is currently disabled."
                        return render(request, 'login.html',
                                      {'form': form, 'msg': msg})
                else:
                    msg = "Incorrect username and / or password."
                    return render(request, 'login.html', {'form': form,
                                                          'msg': msg})
        else:
            form = LoginForm()
            logout(request)
        return render(request, 'login.html', {'form': form, 'status': 200})
    except Exception, e:
        raise e


def log_out(request):
    '''
    Method to handle log out to system
    '''
    try:
        print "User [%s] successfully logged out." % (request.user.username)
        logout(request)
        return HttpResponseRedirect(reverse(home))
    except Exception, e:
        raise e


def register(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        return render(request, 'register.html', {'status': 200})
    except Exception, e:
        raise e


@login_required
@is_allowed_groups(['ACM'])
def roles_home(request):
    '''
    Default page for Roles home
    '''
    try:
        return render(request, 'registry/roles_index.html')
    except Exception, e:
        raise e


@login_required
@is_allowed_groups(['ACM'])
def roles_edit(request, user_id):
    '''
    Create / Edit page for the roles
    '''
    try:
        group_ids = []
        mygrp = request.user.groups.values_list('id', flat=True)
        from django.contrib.auth.models import Group

        # All groups by details as per CPIMS
        cpims_groups = get_groups()
        groups_cpims = dict(zip(cpims_groups.values(), cpims_groups.keys()))

        # Current geo orgs
        ex_areas, ex_orgs = get_allowed_units_county(user_id)
        user = AppUser.objects.get(pk=user_id)
        user_data = {'user_id': user_id}

        vals = {'SMAL': 'Male', 'SFEM': 'Female'}
        person = RegPerson.objects.get(pk=user_id)
        person_extids = RegPersonsExternalIds.objects.filter(person=user_id)
        # Get org units
        person_orgs = RegPersonsOrgUnits.objects.select_related(
            'org_unit_id').filter(person=user_id, is_void=False)
        units_count = person_orgs.count()
        # Get geo locations
        person_geos = RegPersonsGeo.objects.select_related(
            'area').filter(person=user_id, is_void=False)
        county_count = person_geos.count()
        for row in person_extids:
            id_type = row.identifier_type_id
            if id_type == "INTL":
                person.national_id = row.identifier
            if id_type == "IWKF":
                person.workforce_id = row.identifier

        # Forms details
        data = {'orgs-TOTAL_FORMS': units_count,
                'orgs-INITIAL_FORMS': '0',
                'orgs-MAX_NUM_FORMS': ''}
        cnt = 0
        # ex_areas, ex_orgs
        for org_unit in person_orgs:
            org_unit_id = org_unit.org_unit_id.org_unit_id_vis
            org_unit_name = org_unit.org_unit_id.org_unit_name
            unit_name = '%s %s' % (org_unit_id, org_unit_name)
            unit_id = org_unit.org_unit_id.id
            field_prefix = 'orgs-%s' % (cnt)
            data['%s-org_unit_id' % (field_prefix)] = unit_id
            data['%s-org_unit_name' % (field_prefix)] = unit_name
            if unit_id in ex_orgs:
                all_fields = ex_orgs[unit_id]
                for all_field in all_fields:
                    f_name = cpims_groups[all_field]
                    data['%s-%s' % (field_prefix, f_name)] = True
            cnt += 1
        org_form_set = formset_factory(RolesOrgUnits)
        formset = org_form_set(data, prefix='orgs')
        # Geo form set
        gdata = {'areas-TOTAL_FORMS': county_count,
                 'areas-INITIAL_FORMS': '0',
                 'areas-MAX_NUM_FORMS': ''}
        # geo.person.surname
        cnts = 0
        for person_geo in person_geos:
            county_id = person_geo.area.area_id
            county_name = person_geo.area.area_name
            field_prefix = 'areas-%s' % (cnts)
            gdata['%s-area_id' % (field_prefix)] = county_id
            if county_id in ex_areas:
                gdata['%s-area_welfare' % (field_prefix)] = True
            gdata['%s-sub_county' % (field_prefix)] = county_name
            cnts += 1
        geo_form_set = formset_factory(RolesGeoArea)
        gformset = geo_form_set(gdata, prefix='areas')
        # Get all groups

        for cpims_grp in cpims_groups:
            cur_group = cpims_groups[cpims_grp]
            if cpims_grp in mygrp:
                user_data[cur_group] = True
        if user.is_active:
            user_data['activate_choice'] = 'activate'
        if not user.password_changed_timestamp:
            user_data['reset_password'] = True
        form = RolesForm(data=user_data)

        # Lets do the processing down here - Makes sense
        if request.method == 'POST':
            reqs = request.POST
            req_params, sreq_params = {}, {}

            for cntr in range(0, units_count):
                req_params[cntr] = {}
                for req in reqs:
                    val = request.POST.get(req)

                    if req.startswith('orgs-'):
                        fpam = 'orgs-%s-' % (cntr)
                        fvar = str(req.replace(fpam, ''))
                        req_params[cntr][fvar] = val
            # Save org units
            new_units_org = {}
            for oval in range(0, (units_count)):
                org_details = req_params[oval]
                for org_group in groups_cpims:
                    unit_id = int(org_details['org_unit_id'])
                    if org_group in org_details:
                        group_id = groups_cpims[org_group]
                        if unit_id not in new_units_org:
                            new_units_org[unit_id] = []
                        if group_id not in new_units_org[unit_id]:
                                new_units_org[unit_id].append(group_id)

                        save_group_geo_org(user_id, group_id, None, unit_id)
                        if group_id not in group_ids:
                            group_ids.append(group_id)
            # Remove existing and have been removed
            for f_unit in new_units_org:
                new_orgs = new_units_org[f_unit]
                if f_unit in ex_orgs:
                    to_dels = ex_orgs[f_unit]
                    for to_del in to_dels:
                        if to_del not in new_orgs:
                            remove_group_geo_org(user_id, to_del, None, f_unit)
            # Sub county data
            for sntr in range(0, county_count):
                sreq_params[sntr] = {}
                for req in reqs:
                    val = request.POST.get(req)
                    if req.startswith('areas-'):
                        fpam = 'areas-%s-' % (sntr)
                        fvar = str(req.replace(fpam, ''))
                        sreq_params[sntr][fvar] = val
            new_counties = []
            county_grp = groups_cpims['group_SWA']
            for sval in range(0, len(sreq_params)):
                area_details = sreq_params[sval]
                if 'area_welfare' in area_details:
                    area_id = int(area_details['area_id'])
                    new_counties.append(area_id)
                    print 'SAVE', area_id, county_grp, user_id
                    save_group_geo_org(user_id, county_grp, area_id, None)
                    if county_grp not in group_ids:
                        group_ids.append(county_grp)
            # Delete area id groups
            for ex_area in ex_areas:
                if ex_area not in new_counties:
                    remove_group_geo_org(user_id, county_grp, ex_area, None)

            user_id = request.POST.get('user_id')
            sys_config = request.POST.get('group_SCM')
            reg_manager = request.POST.get('group_RGM')
            access_manager = request.POST.get('group_ACM')
            national_welfare = request.POST.get('group_SWM')
            standard_log = request.POST.get('group_STD')
            # Accounts specific
            reset_password = request.POST.get('reset_password')
            activate_choice = request.POST.get('activate_choice')
            if sys_config:
                group_ids.append(groups_cpims['group_SCM'])
            if reg_manager:
                group_ids.append(groups_cpims['group_RGM'])
            if access_manager:
                group_ids.append(groups_cpims['group_ACM'])
            if national_welfare:
                group_ids.append(groups_cpims['group_SWM'])
            if standard_log:
                group_ids.append(groups_cpims['group_STD'])
            # Check if any group is being removed
            removed_groups = list(set(mygrp) - set(group_ids))

            for group_id in group_ids:
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            # Lets remove this groups
            for grp_id in removed_groups:
                group = Group.objects.get(id=grp_id)
                user.groups.remove(group)
            # Lets save password change and activate/deactivate
            if reset_password:
                user.password_changed_timestamp = None
                user.save(update_fields=["password_changed_timestamp"])
            if activate_choice:
                a_choice = True if activate_choice == 'activate' else False
                user.is_active = a_choice
                user.save(update_fields=["is_active"])
            # Redirect will be safe for now
            msg = "Roles modified successfully"
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse(roles_home))

        return render(request, 'registry/roles_edit.html',
                      {'form': form, 'formset': formset,
                       'gformset': gformset, 'person': person,
                       'vals': vals})
    except AppUser.DoesNotExist:
        msg = 'Account must exist to attach a Role / Permission'
        messages.add_message(request, messages.INFO, msg)
        return render(request, 'registry/roles_index.html')
    except RegPerson.DoesNotExist:
        msg = 'Person must exist to attach a Role / Permission'
        messages.add_message(request, messages.INFO, msg)
        return render(request, 'registry/roles_index.html')
    except Exception, e:
        raise e
