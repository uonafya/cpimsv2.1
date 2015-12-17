from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from cpovc_main.functions import (
    get_list_of_org_units, get_dict, get_vgeo_list, get_vorg_list,
    get_persons_list)
from .forms import FormRegistry, FormRegistryNew, FormContact
from .models import RegOrgUnitGeography
from .functions import (
    org_id_generator, save_contacts, save_external_ids, close_org_unit,
    save_geo_location, get_external_ids, get_geo_location, get_contacts,
    get_geo_selected, get_specific_geos)
from cpovc_auth.models import AppUser
from cpovc_registry.models import (
    RegOrgUnit, RegOrgUnitContact, RegPerson, RegPersonsOrgUnits,
    RegPersonsTypes, RegPersonsGuardians, RegPersonsGeo, RegPersonsExternalIds)
from cpovc_registry.forms import (
    RegistrationForm, RegistrationSearchForm, NewUser, UserSearchForm)
from cpovc_main.functions import (
    workforce_id_generator, beneficiary_id_generator, get_org_units_dict)
from cpovc_main.models import SetupGeography
from cpovc_auth.decorators import is_allowed_groups

from django.contrib.auth.models import Group


def home(request):
    '''
    Search page for Organisation Unit / Default page
    '''
    try:
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            if form.is_valid():
                search_string = form.cleaned_data['org_unit_name']
                org_type = form.cleaned_data['org_type']
                org_closed = form.cleaned_data['org_closed']

                closed_org = True if org_closed == 'True' else False
                unit_type = [org_type] if org_type else []
                results = get_list_of_org_units(search_string=search_string,
                                                include_closed=closed_org,
                                                in_org_unit_types=unit_type,
                                                number_of_results=50)
                items = 'result' if len(results) == 1 else 'results'
                ids = []
                for result in results:
                    ids.append(result.id)
                geos = get_specific_geos(ids)
                orgs = {}
                print geos
                for geo in geos:
                    org_id = geo.org_unit_id
                    area_name = geo.area.area_name
                    if org_id not in orgs:
                        orgs[org_id] = [area_name]
                    else:
                        orgs[org_id].append(area_name)
                orgs_name = {}
                print orgs
                for geo in ids:
                    if geo in orgs:
                        gname = orgs[geo]
                        orgs_name[geo] = ' ,'.join(gname)
                    else:
                        orgs_name[geo] = None
                print orgs_name
                message = "Search for %s returned %d %s" % (search_string,
                                                            len(results),
                                                            items)
                check_fields = ['org_unit_type_id']
                val = get_dict(field_name=check_fields)
                # All existing org units
                org_units_list = get_org_units_dict()
                vals = val.copy()
                vals.update(org_units_list)
                return render(request, 'registry/org_units_index.html',
                              {'form': form, 'results': results,
                               'geos': orgs_name,
                               'message': message, 'vals': vals})
            else:
                print 'Not Good %s' % (form.errors)
        form = FormRegistry()
        # groups = request.user.groups.values_list('', flat=True)
        # print groups
        return render(request, 'registry/org_units_index.html',
                      {'form': form})
    except Exception, e:
        print str(e)
        raise e


@is_allowed_groups(['RGM', 'RGU'])
def register_new(request):
    '''
    Create page for New Organisation Unit
    '''
    try:
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            cform = FormContact(data=request.POST)
            print request.POST
            org_unit_type = request.POST.get('org_unit_type')
            org_unit_name = request.POST.get('org_unit_name')
            reg_date = request.POST.get('reg_date')
            if not reg_date:
                reg_date = None
            sub_county = request.POST.getlist('sub_county')
            ward = request.POST.getlist('ward')
            parent_org_unit = request.POST.get('parent_org_unit')
            if not parent_org_unit:
                parent_org_unit = None
            org_reg_type = request.POST.get('org_reg_type')
            legal_reg_number = request.POST.get('legal_reg_number')
            org_new = RegOrgUnit(org_unit_id_vis='NXXXXXX',
                                 org_unit_name=org_unit_name,
                                 org_unit_type_id=org_unit_type,
                                 date_operational=reg_date,
                                 parent_org_unit_id=parent_org_unit,
                                 is_void=False)
            org_new.save()
            org_unit_id = org_new.pk
            org_unit_id_vis = org_id_generator(org_unit_id)
            org_new.org_unit_id_vis = org_unit_id_vis
            org_new.save(update_fields=["org_unit_id_vis"])
            msg = 'Organisation Unit (%s) save success.' % (org_unit_name)
            messages.info(request, msg)
            # Save external ids
            if org_reg_type:
                save_external_ids(org_reg_type, legal_reg_number, org_unit_id)
            # Save geo units
            geo_locs = ward + sub_county
            save_geo_location(geo_locs, org_unit_id)
            # Save contacts
            if cform.is_valid():
                for (form_id, form_value) in cform.extra_contacts():
                    if form_value:
                        print form_id, form_value, org_unit_id
                        save_contacts(form_id, form_value, org_unit_id)
            # Perform audit trail - TO DO
            return HttpResponseRedirect(reverse(home))
        form = FormRegistryNew()
        cform = FormContact()
        return render(request, 'registry/org_units_new.html',
                      {'form': form, 'cform': cform})
    except Exception, e:
        raise e


@is_allowed_groups(['RGM', 'RGU', 'DSU'])
def register_edit(request, org_id):
    '''
    Edit page for Organisation Unit with id - org_id
    '''
    resp = ''
    try:
        units = RegOrgUnit.objects.get(pk=org_id)
        # Geo location ids
        area_ids = get_geo_location(org_id)
        area_list = []
        for area_id in area_ids:
            area_list.append(area_id['area_id'])
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            cform = FormContact(data=request.POST)
            edit_type = int(request.POST.get('edit_org'))
            org_unit_name = request.POST.get('org_unit_name')
            org_unit_type = request.POST.get('org_unit_type')
            reg_date = request.POST.get('reg_date')
            parent_org_unit = request.POST.get('parent_org_unit')
            sub_county = request.POST.getlist('sub_county')
            ward = request.POST.getlist('ward')
            print edit_type
            if edit_type == 1:
                # This is a normal edit
                print 'Normal edit'
                # Update changed fields in main table
                units.org_unit_name = org_unit_name
                units.org_unit_type_id = org_unit_type
                units.date_operational = reg_date
                units.parent_org_unit_id = parent_org_unit
                units.save(update_fields=["org_unit_name"])
                # Update registration details
                org_reg_type = request.POST.get('org_reg_type')
                reg_number = request.POST.get('legal_reg_number')
                if org_reg_type:
                    save_external_ids(org_reg_type, reg_number, org_id)
                # Update Geo locations
                geo_locs = ward + sub_county
                save_geo_location(geo_locs, org_id, area_list)
                # Update contacts
                if cform.is_valid():
                    for (form_id, form_value) in cform.extra_contacts():
                        if form_value:
                            save_contacts(form_id, form_value, org_id)
            elif edit_type == 2:
                # This is a close with date provided
                close_date = request.POST.get('close_date')
                if close_date:
                    close_org_unit(close_date, org_id)
                resp = 'Closed with given date - %s' % (close_date)
            else:
                # This is a close without date - use today
                close_org_unit(None, org_id)
                resp = 'Closed due to error / duplicate'
            msg = 'Organisation Unit (%s) edit success.' % (org_unit_name)
            msg += '\n%s' % (resp)
            messages.info(request, msg)
            # org_unit_name = form.cleaned_data['org_unit_name']
            '''
            # results = {'message': msg, 'value': org_unit_type}
            # return JsonResponse(results, content_type='application/json')
            '''
            return HttpResponseRedirect(reverse(home))
        # f = ContactForm(request.POST, initial=data)
        # f.has_changed()
        name = units.org_unit_name
        unit_type = units.org_unit_type_id
        date_op = units.date_operational
        date_closed = units.date_closed
        parent_unit = units.parent_org_unit_id
        # External ids
        ext_ids = get_external_ids(org_id)
        external = {}
        if ext_ids:
            reg_type = ext_ids[0]['identifier_type_id']
            reg_number = ext_ids[0]['identifier_value']
            external['org_reg_type'] = reg_type
            external['legal_reg_number'] = reg_number
        data_dict = external.copy()
        # Final data
        data = {'org_unit_name': name, 'org_unit_type': unit_type,
                'reg_date': date_op, 'sub_county': area_list,
                'ward': area_list, 'close_date': date_closed,
                'parent_org_unit': parent_unit}
        data_dict.update(data)
        form = FormRegistryNew(data_dict)
        # Get contact details
        contacts = get_contacts(org_id)
        print contacts
        cform = FormContact(contacts)
        return render(request,
                      'registry/org_units_edit.html', {'form': form,
                                                       'cform': cform})
    except RegOrgUnit.DoesNotExist:
        form = FormRegistry()
        msg = 'Organisation Unit does not exist'
        messages.add_message(request, messages.INFO, msg)
        return render(request, 'registry/org_units_index.html',
                      {'form': form})
    except Exception, e:
        # raise e
        form = FormRegistry()
        msg = 'Organisation Unit does not exist - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return render(request, 'registry/org_units_index.html',
                      {'form': form})


def register_details(request, org_id):
    '''
    Some default page for the home page / Dashboard
    vals - All possible list_general used on this page
    '''
    try:
        # All my filters
        check_fields = ['contact_detail_type_id', 'org_unit_type_id',
                        'identifier_type_id']
        val = get_dict(field_name=check_fields)
        # All existing org units
        org_units_list = get_org_units_dict()
        vals = val.copy()
        vals.update(org_units_list)
        org_unit = RegOrgUnit.objects.get(pk=org_id)
        org_contact = RegOrgUnitContact.objects.filter(org_unit_id=org_id)
        org_unit.contacts = org_contact
        # Geo details
        inner_qs = RegOrgUnitGeography.objects.filter(
            org_unit_id=org_id).values('area_id')
        entries = SetupGeography.objects.filter(area_id__in=inner_qs)
        wards, sub_counties = [], []
        for inner_q in entries:
            area_type = inner_q.area_type_id
            area_name = inner_q.area_name
            if area_type == 'GDIS':
                sub_counties.append(area_name)
            if area_type == 'GWRD':
                wards.append(area_name)
        show_wards = ' ,'.join(wards)
        show_county = ' ,'.join(sub_counties)
        # External ids
        ext_ids = get_external_ids(org_id)
        if ext_ids:
            reg_type = ext_ids[0]['identifier_type_id']
            reg_number = ext_ids[0]['identifier_value']
            org_unit.registration_type = reg_type
            org_unit.registration_number = reg_number
        org_unit.sub_county = show_county
        org_unit.wards = show_wards
        return render(request, 'registry/org_units_details.html',
                      {'org_details': org_unit, 'vals': vals})
    except Exception, e:
        # raise e
        error = 'Org unit view error - %s' % (str(e))
        print error
        form = FormRegistry()
        msg = 'Organisation Unit does not exist - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return render(request, 'registry/org_units_index.html',
                      {'form': form})


@is_allowed_groups(['RGM'])
def new_person(request):
    operation_msg = None

    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)

        try:
            designation = request.POST.get('cadre_type')
            person_type = request.POST.getlist('person_type')
            first_name = request.POST.get('first_name')
            other_names = request.POST.get('other_names')
            surname = request.POST.get('surname')
            sex_id = request.POST.get('sex_id')
            des_phone_number = request.POST.get('des_phone_number')
            email = request.POST.get('email')
            living_in = request.POST.get('living_in')
            org_units = request.POST.getlist('org_unit_id')
            relationships = request.POST.getlist('relationship_type_id')

            national_id = request.POST.get('national_id')
            staff_id = request.POST.get('staff_id')
            birth_reg_id = request.POST.get('birth_reg_id')
            caregiver_id = request.POST.get('caregiver_id')

            date_of_birth = request.POST.get('date_of_birth')
            date_of_death = request.POST.get('date_of_death')

            # Capture RegPerson Model
            person = RegPerson(
                designation=designation.upper(),
                first_name=first_name.upper(),
                other_names=other_names.upper(),
                surname=surname.upper(),
                sex_id=sex_id,
                des_phone_number=des_phone_number,
                email=email,
                date_of_birth=date_of_birth,
                date_of_death=None,
                is_void=False)

            person.save()

            reg_person_pk = int(person.pk)

            # Capture RegPersonTypes Model
            if person_type:
                now = timezone.now()
                for i, _person_type in enumerate(person_type):
                    RegPersonsTypes(
                        person=RegPerson.objects.get(pk=int(reg_person_pk)),
                        person_type_id=_person_type,
                        date_began=now,
                        date_ended=None,
                        is_void=False).save()

            # Capture RegPersonsOrgUnits Model
            if org_units:
                for i, _org_unit in enumerate(org_units):
                    RegPersonsOrgUnits(
                        person=RegPerson.objects.get(pk=int(reg_person_pk)),
                        org_unit_id=RegOrgUnit.objects.get(pk=int(_org_unit)),
                        date_linked=now,
                        date_delinked=None,
                        is_void=False).save()

            # Capture RegPersonsGeo Model
            if living_in:
                area_id = living_in
                RegPersonsGeo(
                    person=RegPerson.objects.get(
                        pk=int(reg_person_pk)),
                    area_id=area_id,
                    date_linked=now,
                    date_delinked=None,
                    is_void=False).save()

            # Capture RegPersonsGuardians Model
            if relationships:
                for i, _relationship in enumerate(relationships):
                    RegPersonsGuardians(
                        child_person=RegPerson.objects.get(
                            pk=int(reg_person_pk)),
                        guardian_person_id=caregiver_id,
                        relationship=_relationship,
                        date_linked=now,
                        date_delinked=None,
                        is_void=False).save()

            # Capture RegPersonsExternalIds Model
            identifier = None
            identifier_type_id = None
            wfc_list = []
            workforce_id = None
            beneficiary_id = None
            identifier_types = []

            if person_type:
                wfc_list = person_type
                if any(['TWGE' in wfc_list, 'TWNE' in wfc_list, 'TWVL' in wfc_list]):
                    workforce_id = workforce_id_generator(reg_person_pk)
                if ('TBGR' in wfc_list):
                    beneficiary_id = beneficiary_id_generator(reg_person_pk)
                if national_id:
                    identifier_types.append('INTL')
                if staff_id:
                    identifier_types.append('IMAN')
                if workforce_id:
                    identifier_types.append('IWKF')
                if beneficiary_id:
                    identifier_types.append('ISCG')
                if birth_reg_id:
                    identifier_types.append('ISOV')

                for i, identifier_type in enumerate(identifier_types):
                    if identifier_type == 'INTL':
                        identifier = national_id
                    if identifier_type == 'IMAN':
                        identifier = staff_id
                    if identifier_type == 'IWKF':
                        identifier = workforce_id
                    if identifier_type == 'ISCG':
                        identifier = beneficiary_id
                    if identifier_type == 'ISOV':
                        identifier = birth_reg_id

                    RegPersonsExternalIds(
                        person=RegPerson.objects.get(pk=int(reg_person_pk)),
                        identifier_type_id=identifier_type,
                        identifier=identifier,
                        is_void=False).save()

        except Exception, e:
            operation_msg = 'An error occured when saving data -  %s' % (
                str(e))
            messages.add_message(request, messages.INFO, operation_msg)
            return render(request, 'registry/new_person.html', {'form': form},)

        operation_msg = 'Person (%s) save success.' % first_name.upper()
        messages.add_message(request, messages.INFO, operation_msg)
        return HttpResponseRedirect(reverse(persons_search))
    else:
        # Not request.POST
        form = RegistrationForm()
        return render(request, 'registry/new_person.html', {'form': form},)


def persons_search(request):
    '''
    Some default page for the home page / Dashboard
    '''
    res = None
    resultsets = None
    resultset = None
    results = None
    result = None
    wfc_type = None
    person_type = None
    search_location = False
    search_wfc_by_org_unit = False
    app_user = {}

    try:
        if request.method == 'POST':
            form = RegistrationSearchForm(data=request.POST)
            if form.is_valid():

                check_fields = [
                    'sex_id', 'cadre_type_id', 'person_type_id', 'relationship_type_id', 'identifier_type_id']
                vals = get_dict(field_name=check_fields)

                person_type = form.cleaned_data['person_type']
                search_string = form.cleaned_data['search_name']
                person_deceased = form.cleaned_data['person_deceased']
                search_criteria = form.cleaned_data['search_criteria']

                deceased_person = True if person_deceased == 'True' else False
                type_of_person = [person_type] if person_type else []

                # Make PersonType selection mandatory
                if person_type:
                    wfc_type = person_type

                # Filter Location Searches
                if search_criteria == 'ORG':
                    search_wfc_by_org_unit = True
                if search_criteria == 'RES':
                    search_location = True

                resultsets = get_persons_list(user=request.user, tokens=search_string, wfc_type=wfc_type,
                                              search_location=search_location, search_wfc_by_org_unit=search_wfc_by_org_unit)

                check_fields = [
                    'sex_id', 'cadre_type_id', 'person_type_id', 'relationship_type_id', 'identifier_type_id']
                vals = get_dict(field_name=check_fields)

                result_pk = None
                pgeolocs_ = None
                porgs_ = None
                if resultsets:
                    for resultset in resultsets:
                        if resultset:
                            for result in resultset:
                                result_pk = result.pk

                                person_types = RegPersonsTypes.objects.filter(
                                    person=result_pk)
                                person_geos = RegPersonsGeo.objects.filter(
                                    person=result_pk)
                                person_orgs = RegPersonsOrgUnits.objects.filter(
                                    person=result_pk)

                                result.ptypes = person_types
                                result.pgeos = person_geos
                                result.porgs = person_orgs

                                for person_geo in person_geos:
                                    pgeolocs_ = get_vgeo_list(
                                        person_geo.area_id)

                                for person_org in person_orgs:
                                    porgs_ = get_vorg_list(
                                        person_org.org_unit_id_id)

                                result.pgeolocs = pgeolocs_
                                result.porgs = porgs_
                        accounts = AppUser.objects.all().values(
                            'id', 'reg_person_id')
                        for account in accounts:
                            account_id = 'U%s' % (account['id'])
                            app_user[account['reg_person_id']] = account_id
                        print accounts
                    return render(request, 'registry/persons_search.html',
                                  {'form': form, 'resultsets': resultsets,
                                   'vals': vals, 'person_type': person_type,
                                   'app_user': app_user})
                else:
                    messages.add_message(
                        request, messages.ERROR, 'Person not found!')
                    return HttpResponseRedirect(reverse(persons_search))
            else:
                print 'Not Good %s' % (form.errors)
        form = RegistrationSearchForm()
        return render(request, 'registry/persons_search.html',
                      {'form': form, 'result': result, 'person_type': person_type})
    except Exception, e:
        raise e


def view_person(request, id):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        # All my filters
        #check_fields = ['cadre_type_id', 'person_type_id', area_id, org_unit_id, 'relationship_type_id']
        check_fields = ['sex_id', 'cadre_type_id', 'person_type_id',
                        'relationship_type_id', 'identifier_type_id']
        vals = get_dict(field_name=check_fields)
        pgeolocs_ = None

        person = RegPerson.objects.get(pk=id)
        person_types = RegPersonsTypes.objects.filter(person=person)
        person_geos = RegPersonsGeo.objects.filter(person=person)
        person_orgs = RegPersonsOrgUnits.objects.filter(person=person)
        person_extids = RegPersonsExternalIds.objects.filter(person=person)

        # Check if has an account
        user_id = None
        try:
            users = AppUser.objects.get(reg_person=person)
            user_id = users.pk
        except Exception:
            pass

        person.ptypes = person_types
        person.pgeos = person_geos
        person.porgs = person_orgs
        person.pextids = person_extids

        for person_geo in person_geos:
            pgeolocs_ = get_vgeo_list(person_geo.area_id)

        for person_org in person_orgs:
            porgs_ = get_vorg_list(person_org.org_unit_id_id)

        person.pgeolocs = pgeolocs_
        person.porgs = porgs_
        person.person_id = user_id

        return render(request, 'registry/view_person.html',
                      {'person_details': person,
                       'vals': vals})
    except Exception, e:
        # raise e
        msg = 'Person does not exist - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(persons_search))

    form = RegistrationForm()
    return render(request, 'registry/view_person.html', {'form': form},)


@is_allowed_groups(['RGM'])
def edit_person(request, id):
    '''
    Some default page for the home page / Dashboard
    '''
    if request.method == 'POST':
        try:
            form = RegistrationForm(data=request.POST)
            person_type = request.POST.getlist('person_type')
            first_name = request.POST.get('first_name')
            other_names = request.POST.get('other_names')
            surname = request.POST.get('surname')
            sex_id = request.POST.get('sex_id')
            des_phone_number = request.POST.get('des_phone_number')
            email = request.POST.get('email')
            living_in = request.POST.get('living_in')
            date_of_birth = request.POST.get('date_of_birth')
            org_units = request.POST.getlist('org_unit_id')
            relationships = request.POST.getlist('relationship_type_id')
            national_id = request.POST.get('national_id')
            staff_id = request.POST.get('staff_id')
            birth_reg_id = request.POST.get('birth_reg_id')
            caregiver_id = request.POST.get('caregiver_id')
            date_of_birth = request.POST.get('date_of_birth')
            date_of_death = request.POST.get('date_of_death')

            now = timezone.now()

            # Update RegPerson
            operson = RegPerson.objects.get(pk=id)
            operson.first_name = first_name
            operson.other_names = other_names
            operson.surname = surname
            operson.sex_id = sex_id
            operson.des_phone_number = des_phone_number
            operson.email = email
            operson.date_of_birth = date_of_birth
            operson.save(update_fields=['first_name', 'other_names', 'surname', 'sex_id',
                                        'des_phone_number', 'email', 'date_of_birth'])

            # Update RegPersonsGeo
            opersongeos = RegPersonsGeo.objects.filter(pk=id)
            for opersongeo in opersongeos:
                opersongeo.is_void = True
                opersongeo.save(update_fields=['is_void'])
                RegPersonsGeo(
                    person=RegPerson.objects.get(
                        pk=int(id)),
                    area_id=living_in,
                    date_linked=now,
                    date_delinked=None,
                    is_void=False).save()

            # Update RegPersonsOrgUnits Model
            if org_units:
                opersonorgus = RegPersonsOrgUnits.objects.filter(person=id)

                for opersonorgu in opersonorgus:
                    if not str(opersonorgu.org_unit_id_id) in org_units:
                        opersonorgu.is_void = True
                        opersonorgu.date_delinked = now
                        opersonorgu.save(
                            update_fields=['is_void', 'date_delinked'])
                for i, _org_unit in enumerate(org_units):
                    opersonorgu_ = RegPersonsOrgUnits.objects.filter(
                        pk=id, org_unit_id_id=_org_unit)
                    if not opersonorgu_:
                        RegPersonsOrgUnits(
                            person=RegPerson.objects.get(pk=int(id)),
                            org_unit_id=RegOrgUnit.objects.get(
                                pk=int(_org_unit)),
                            date_linked=now,
                            date_delinked=None,
                            is_void=False).save()

            # Capture RegPersonsExternalIds Model
            """ To factor external ids update on persontype changed """
            pk = None
            identifier = None
            identifier_type_id = None
            wfc_list = []
            workforce_id = None
            beneficiary_id = None
            identifier_types = []
            personids = RegPersonsExternalIds.objects.filter(person=id)

            if national_id:
                identifier_types.append('INTL')
            if staff_id:
                identifier_types.append('IMAN')
            if workforce_id:
                identifier_types.append('IWKF')
            if beneficiary_id:
                identifier_types.append('ISCG')
            if birth_reg_id:
                identifier_types.append('ISOV')

            print identifier_types

            for personid in personids:
                pk = personid.pk
                if person_type:
                    wfc_list = person_type
                if any(['TWGE' in wfc_list, 'TWNE' in wfc_list, 'TWVL' in wfc_list]):
                    workforce_id = workforce_id_generator(pk)
                if ('TBGR' in wfc_list):
                    beneficiary_id = beneficiary_id_generator(pk)

                for i, identifier_type in enumerate(identifier_types):
                    if identifier_type == 'INTL':
                        identifier = national_id
                    if identifier_type == 'IMAN':
                        identifier = staff_id
                    if identifier_type == 'IWKF':
                        identifier = workforce_id
                    if identifier_type == 'ISCG':
                        identifier = beneficiary_id
                    if identifier_type == 'ISOV':
                        identifier = birth_reg_id

                    personid.identifier_type_id = identifier_type
                    personid.identifier = identifier
                    personid.save(
                        update_fields=['identifier_type_id', 'identifier'])

                    identifier_types.remove(identifier_type)

            msg = 'Update of Person(%s) successful.' % first_name
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse(persons_search))

        except Exception, e:
            # raise e
            msg = 'Person update error - %s' % (str(e))
            messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(persons_search))
    else:
        person = None
        person_type_id = None
        try:
            person = RegPerson.objects.get(pk=id)
            person_types = RegPersonsTypes.objects.filter(person=person)
            person_geos = RegPersonsGeo.objects.filter(person=person)
            person_orgs = RegPersonsOrgUnits.objects.filter(person=person)
            person_extids = RegPersonsExternalIds.objects.filter(person=person)

            person.ptypes = person_types
            person.pgeos = person_geos
            person.porgs = person_orgs
            person.pextids = person_extids

            for ptype in person.ptypes:
                person_type_id = ptype.person_type_id

            for pgeo in person.pgeos:
                living_in = pgeo.area_id

            for porg in person.porgs:
                porgs_ = get_vorg_list(porg.org_unit_id_id)

            # Get extid values
            national_id_ = ''
            staff_id_ = ''
            workforce_id_ = ''
            caregiver_id_ = ''
            birth_reg_id_ = ''
            for pextid in person.pextids:
                pextid_identifier_type = pextid.identifier_type_id
                pextid_identifier = pextid.identifier

                if pextid_identifier_type == 'INTL':
                    national_id_ = pextid_identifier
                if pextid_identifier_type == 'IMAN':
                    staff_id_ = pextid_identifier
                # if pextid_identifier_type == 'IWKF':
                #    workforce_id_ = pextid_identifier
                if pextid_identifier_type == 'ISCG':
                    caregiver_id_ = pextid_identifier
                if pextid_identifier_type == 'ISOV':
                    birth_reg_id_ = pextid_identifier

            # Get orgunit values
            org_unit_id_ = None
            for porg_ in porgs_:
                unit_id_ = porg_.id

            form = RegistrationForm(initial={
                'person_type': person_type_id,
                'cadre_type': person.designation,
                'first_name': person.first_name,
                'other_names': person.other_names,
                'surname': person.surname,
                'sex_id': person.sex_id,
                'des_phone_number': person.des_phone_number,
                'date_of_birth': person.date_of_birth,
                'email': person.email,
                'living_in': living_in,
                'org_unit_id': unit_id_,
                'national_id': national_id_,
                'staff_id': staff_id_,
                'birth_reg_id': birth_reg_id_,
                'caregiver_id': caregiver_id_
            })
            return render(request, 'registry/edit_person.html', {'form': form, 'pk': person.pk, 'person_type': person_type_id})
        except Exception, e:
            msg = 'Person does not exist - %s' % (str(e))
            messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(persons_search))


def delete_person(request, id):
    '''
    Some default page for the home page / Dashboard
    '''
    first_name = None
    surname = None
    try:
        # Delete from RegPerson
        person = RegPerson.objects.get(pk=id)
        person.is_void = True
        first_name = person.first_name
        surname = person.surname
        person.save(update_fields=['is_void'])

        # Delete from RegPersonsTypes
        persontype = RegPersonsTypes.objects.get(pk=id)
        persontype.is_void = True
        persontype.save(update_fields=['is_void'])

        # Delete from RegPersonsOrgUnits
        personorgunits = RegPersonsOrgUnits.objects.filter(person=id)
        for personorgunit in personorgunits:
            personorgunit.is_void = True
            personorgunit.save(update_fields=['is_void'])

        # Delete from RegPersonsGeo
        persongeos = RegPersonsGeo.objects.filter(person=id)
        for persongeo in persongeos:
            persongeo.is_void = True
            persongeo.save(update_fields=['is_void'])

        # Delete from RegPersonsGuardians
        personguardians = RegPersonsGuardians.objects.filter(
            child_person_id=id)
        for personguardian in personguardians:
            personguardian.is_void = True
            personguardian.save(update_fields=['is_void'])

        # Delete from RegPersonsExternalIds
        personextids = RegPersonsExternalIds.objects.filter(person=id)
        for personextid in personextids:
            personextid.is_void = True
            personextid.save(update_fields=['is_void'])

        msg = 'Delete (%s %s) successful.' % (first_name, surname)
        messages.add_message(request, messages.INFO, msg)
    except Exception, e:
        msg = 'Delete error - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(persons_search))

# WORKFORCE


def new_user(request):
    '''
    Some default page for the home page / Dashboard
    '''

    msg = ''
    password = ''

    if request.method == 'POST':
        form = NewUser(data=request.POST)

        try:
            person_id = request.POST.get('person_id')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Get Name
            person = RegPerson.objects.get(pk=person_id)
            personfname = person.first_name
            personsname = person.surname

            # resolve existing account
            user_exists = AppUser.objects.filter(reg_person=person_id)
            if user_exists:
                msg = 'Person (%s %s) has an existing user account.' % (
                    personfname, personsname)
                messages.add_message(request, messages.INFO, msg)
                return HttpResponseRedirect(reverse(persons_search))

            if password1 == password2:
                password = password1
            else:
                msg = 'Passwords do not match!'
                messages.add_message(request, messages.INFO, msg)
                form = NewUser(data=request.POST)
                return render(request, 'registry/new_user.html',
                              {'form': form},)

            # validate username if__exists
            username_exists = AppUser.objects.filter(username=username)
            if username_exists:
                msg = 'The username (%s) is taken.Pick another one.' % username
                messages.add_message(request, messages.INFO, msg)
                form = NewUser(data=request.POST)
                return render(request, 'registry/new_user.html',
                              {'form': form},)
            else:
                # Create User
                user = AppUser.objects.create_user(username=username,
                                                   reg_person=person_id,
                                                   password=password)
                if user:
                    user.groups.add(Group.objects.get(name='Standard logged in'))
                    # Capture msg & op status
                    msg = 'User (%s) save success.' % (username)
                    messages.add_message(request, messages.INFO, msg)
                    return HttpResponseRedirect(reverse(workforce_search))

        except Exception, e:
            msg = 'Error - (%s) ' % (str(e))
            # Capture msg & op status
            messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(reverse(persons_search))
    else:
        form = NewUser()
        return render(request, 'registry/new_user.html', {'form': form},)


def workforce_search(request):
    res = None
    resultsets = None
    resultset = None
    results = None
    result = None
    wfc_type = None
    person_type = None
    search_location = False
    search_wfc_by_org_unit = False

    if request.method == 'POST':
        form = UserSearchForm(data=request.POST)
        try:
            if form.is_valid():
                person_type = form.cleaned_data['person_type']
                search_string = form.cleaned_data['search_name']
                person_deceased = form.cleaned_data['person_deceased']
                search_criteria = form.cleaned_data['search_criteria']

                deceased_person = True if person_deceased == 'True' else False
                type_of_person = [person_type] if person_type else []

                # Make PersonType selection mandatory
                if person_type:
                    wfc_type = person_type

                # Filter Location Searches
                if search_criteria == 'ORG':
                    search_wfc_by_org_unit = True
                if search_criteria == 'RES':
                    search_location = True

                resultsets = get_persons_list(user=request.user, tokens=search_string, wfc_type=wfc_type,
                                              search_location=search_location, search_wfc_by_org_unit=search_wfc_by_org_unit)

                result_pk = None
                pgeolocs_ = None
                porgs_ = None
                if resultsets:
                    for resultset in resultsets:
                        if resultset:
                            for result in resultset:
                                result_pk = result.pk
                                users = AppUser.objects.filter(
                                    reg_person_id=result_pk)
                                result.appusers = users
                return render(request, 'registry/workforce_search.html',
                              {'resultsets': resultsets, 'form': form})
        except Exception, e:
            msg = 'Error - (%s) ' % (str(e))
            messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(reverse(workforce_search))
        form = UserSearchForm()
        return render(request, 'registry/workforce_search.html', {'form': form})
    else:
        form = UserSearchForm()
        return render(request, 'registry/workforce_search.html', {'form': form})


def registry_look(request):
    '''
    Json lookup stuff
    '''
    try:
        msg, selects = 'Test', ''
        results = {'message': msg}
        if request.method == 'POST':
            county = request.POST.getlist('county[]')
            sub_county = request.POST.getlist('sub_county[]')
            ward = request.POST.getlist('ward[]')
            action = int(request.POST.get('action'))
            datas = sub_county if action == 1 else county
            extras = ward if action == 1 else sub_county
            print action, datas, extras
            results = get_geo_selected(results, datas, extras)
            res_extras = map(str, extras)
            if res_extras:
                selects = ','.join(res_extras)
            results['selects'] = selects
            print results
        return JsonResponse(results, content_type='application/json',
                            safe=False)
    except Exception, e:
        raise e
