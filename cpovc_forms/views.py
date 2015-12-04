from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from cpovc_forms.forms import (OVCSearchForm, OVCDetailsForm)
from cpovc_main.functions import (
    get_list_of_org_units, get_dict, get_vgeo_list, get_vorg_list, get_persons_list)
from cpovc_registry.models import (
    RegOrgUnit, RegOrgUnitContact, RegPerson, RegPersonsOrgUnits,
    RegPersonsTypes, RegPersonsGuardians, RegPersonsGeo, RegPersonsExternalIds)


def forms_home(request):
    '''
    Some default page for forms home page
    '''
    try:
        form = OVCSearchForm(initial={'person_type': 'TBVC'})
        return render(request, 'forms/forms_index.html', {'status': 200, 'form': form})
    except Exception, e:
        raise e


def case_record_sheet(request, formtype):
    '''
    Some default page for forms home page
    '''
    try:
        form = OVCDetailsForm()
        return render(request, 'forms/case_record_sheet.html', {'form': form})
    except Exception, e:
        raise e

def ovc_search(request):

    if request.method == 'POST':
        resultsets = None
        resultset = None
        result = None
        wfc_type = None
        person_type = None
        search_location = False
        search_wfc_by_org_unit = False

        try:
            form = OVCSearchForm(data=request.POST, initial={'person_type': 'TBVC'})
            check_fields = ['sex_id', 'cadre_type_id', 'person_type_id',
                            'relationship_type_id', 'identifier_type_id']
            vals = get_dict(field_name=check_fields)

            person_type = request.POST.get('person_type')
            search_string = request.POST.get('search_name')
            search_criteria = request.POST.get('search_criteria')

            # Preselect PersonType selection mandatory
            if person_type:
                wfc_type = 'TBVC'

            # Filter Location Searches
            if search_criteria == 'ORG':
                search_wfc_by_org_unit = True
            if search_criteria == 'RES':
                search_location = True

            resultsets = get_persons_list(user=request.user, tokens=search_string, wfc_type=wfc_type,
                                          search_location=search_location, search_wfc_by_org_unit=search_wfc_by_org_unit)

            check_fields = ['sex_id', 'cadre_type_id', 'person_type_id',
                            'relationship_type_id', 'identifier_type_id']
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
                                pgeolocs_ = get_vgeo_list(person_geo.area_id)

                            for person_org in person_orgs:
                                porgs_ = get_vorg_list(
                                    person_org.org_unit_id_id)

                            result.pgeolocs = pgeolocs_
                            result.porgs = porgs_

            return render(request, 'forms/forms_index.html',
                          {'form': form, 'resultsets': resultsets, 'vals': vals, 'person_type': person_type})
        except Exception, e:
            msg = 'OVC search error - %s' % (str(e))
            messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(ovc_search))
    else:
        form = OVCSearchForm(initial={'person_type': 'TBVC'})
        return render(request, 'forms/forms_index.html',
                      {'form': form})
