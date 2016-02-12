from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers
from django.conf import settings
from django.db.models import Q
import json
import operator
import random
import uuid
# from itertools import chain
from datetime import datetime
from shutil import copyfile
from cpovc_forms.forms import (
    OVCSearchForm, OVC_FT3hForm, SearchForm, OVC_CaseEventForm, DocumentsManager)
from cpovc_forms.models import (OVCDetails, OVCReferral, OVCHobbies, OVCFriends, OVCDocuments,
                                OVCMedical, OVCCaseRecord, OVCNeeds, OVCCaseCategory, OVCInterventions,
                                FormsAuditTrail, OVCCaseEvents, OVCCaseEventServices, OVCCaseEventCourt,
                                OVCCaseEventPlacement, OVCCaseClosure)
from cpovc_main.functions import (
    get_list_of_org_units, get_dict, get_vgeo_list, get_vorg_list, get_persons_list, form_id_generator,
    case_event_id_generator, convert_date, new_guid_32, beneficiary_id_generator)
from cpovc_registry.models import (
    RegOrgUnit, RegOrgUnitContact, RegPerson, RegPersonsOrgUnits, AppUser,
    RegPersonsTypes, RegPersonsGuardians, RegPersonsGeo, RegPersonsExternalIds)
from cpovc_main.models import (SetupList)


jsonObjectArray = []

"""
def json_serial(obj):
    **JSON serializer for objects not serializable by default json code**
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    if isinstance(obj, unicode):
        return str(serial)
    raise TypeError("Type not serializable")
"""

def translate(value):
    item_value = SetupList.objects.get(item_id=value, is_void=False)
    return item_value.item_description

def forms_home(request):
    '''
    Some default page for forms home page
    '''
    try:
        # results = OVCCaseCategory.objects.
        form = OVCSearchForm(initial={'person_type': 'TBVC'})
        return render(request, 'forms/forms_index.html', {'status': 200, 'form': form})
    except Exception, e:
        raise e


def forms_registry(request):
    personsets = set()
    resultsets = set()
    tmp_result = None
    wfc_type = 'TBVC'
    search_location = False  # We shall not search OVC by Residence
    search_wfc_by_org_unit = False  # We shall not search OVC by OrgUnit

    try:
        if request.method == 'POST':
            form = SearchForm(data=request.POST)
            form_type = request.POST.get('form_type')
            form_owner = request.POST.get('form_person')

            tmp_result = FormsAuditTrail.objects.filter(
                form_type_id=form_type,
                is_void=False)

            if form_owner:
                personsets = get_persons_list(user=request.user,
                                              tokens=form_owner,
                                              wfc_type=wfc_type,
                                              search_location=search_location,
                                              search_wfc_by_org_unit=search_wfc_by_org_unit)
                for set_ in personsets:
                    if len(set_) > 0:
                        for personset in personsets:
                            for person in personset:
                                tmp_result = FormsAuditTrail.objects.filter(
                                    form_type_id=form_type,
                                    person_id=person.pk,
                                    is_void=False)
                                msg = 'Showing results for %s form (Owner: %s)' % (
                                    form_type, form_owner.upper())
                                messages.add_message(
                                    request, messages.INFO, msg)
                    else:
                        msg = 'Search returned 0 results.Displaying all forms.'
                        messages.add_message(request, messages.INFO, msg)

            for f in tmp_result:
                resultsets.add(tmp_result)

            for resultset in resultsets:
                for result in resultset:
                     # Get Person
                    people = RegPerson.objects.filter(pk=int(result.person_id))
                    result.persons = people

                    # Get OrgUnit
                    porgs_ = None
                    orgunits = RegPersonsOrgUnits.objects.filter(
                        person=int(result.person_id))
                    for orgunit in orgunits:
                        # print 'orgunit.org_unit_id ------ %s'
                        # %orgunit.org_unit_id
                        porgs_ = get_vorg_list(orgunit.org_unit_id)
                    result.orgunit = porgs_

                    # Get Case Serial
                    case_records = OVCCaseRecord.objects.filter(
                        case_id=result.form_id)
                    result.case_record = case_records

            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)

            return render(request, 'forms/forms_registry.html', {'form': form,
                                                                 'resultsets': resultsets,
                                                                 'vals': vals})
        else:
            print 'forms_registry: NOT POST'
    except Exception, e:
        print 'Error: %s' % str(e)
    form = SearchForm()
    return render(request, 'forms/forms_registry.html', {'form': form})


def documents_manager_search(request):
    resultsets = None
    resultset = None
    result = None
    wfc_type = None
    person_type = None
    search_location = False
    search_wfc_by_org_unit = False
    try:
        if request.method == 'POST':
            form = DocumentsManager(data=request.POST)
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
                                    person_org.org_unit_id)

                            result.pgeolocs = pgeolocs_
                            result.porgs = porgs_
            return render(request, 'forms/documents_manager.html',
                          {'form': form, 'resultsets': resultsets, 'vals': vals, 'person_type': person_type})
        else:
            print 'Not $POST'
    except Exception, e:
        msg = 'DocumentsManager Child/Person Search Error - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(ovc_search))
    form = DocumentsManager()
    return render(request, 'forms/documents_manager.html', {'form': form})


def documents_manager(request):
    try:
        if request.method == 'POST':
            document_dest_dir = settings.DOCUMENTS_URL
            person_id = request.POST.get('person')
            document_type = request.POST.get(
                'document_type')
            document_description = request.POST.get(
                'document_description')
            file_name = request.POST.get(
                'file_name')
            file_contents = request.FILES.get(
                'file_browser')

            # Read FileContents
            file_rand = random.randint(100000, 999999)
            now = timezone.now()
            dest_file_name = file_name + '_' + \
                str(file_rand) + '_person_' + str(person_id)
            full_path = document_dest_dir + '/' + dest_file_name

            # Write Documents to destination
            with open(full_path, 'wb+') as destination:
                for chunk in file_contents.chunks():
                    destination.write(chunk)

            # Save Documents(metadata)
            document_dir = full_path
            document_name = file_name
            person_id = int(person_id)
            OVCDocuments(
                document_type=document_type,
                document_description=document_description,
                document_name=document_name,
                document_dir=document_dir,
                person=RegPerson.objects.get(pk=person_id)).save()
            msg = 'Document(s) Save Successfull'
            messages.add_message(request, messages.INFO, msg)
            return HttpResponseRedirect(reverse(documents_manager))
        else:
            print 'Not $POST'
    except Exception, e:
        msg = 'Document(s) Save Error - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(documents_manager))
    form = DocumentsManager()
    return render(request, 'forms/documents_manager.html', {'form': form})

    return render(request, 'forms/documents_manager.html', {'status': 200, 'form': form})


def edit_case_record_sheet(request, id):
    try:
        if request.method == 'POST':
            print '[POSTING to view: edit_case_record_sheet]'
        else:
            # Get OVCCaseRecord
            results_case = OVCCaseRecord.objects.get(case_id=id)

            # Get OVCDetails
            results = OVCDetails.objects.get(case_id=id)

            # Get OVCMedical
            results_med = OVCMedical.objects.get(case_id=id)

            # Get OVCFriends
            results_frnds = OVCFriends.objects.filter(case_id=id)
            results_frnd = []
            for result_frnds in results_frnds:
                result_frnds_fname = str(result_frnds.friend_firstname)
                result_frnds_oname = str(result_frnds.friend_other_names)
                result_frnds_lname = str(result_frnds.friend_surname)

                result_frnds_name = result_frnds_fname
                if not result_frnds_oname == 'XXXX':
                    result_frnds_name = result_frnds_name + \
                        ' ' + result_frnds_oname
                if not result_frnds_lname == 'XXXX':
                    result_frnds_name = result_frnds_name + \
                        ' ' + result_frnds_lname
                results_frnd.append(result_frnds_name)

            # Get OVCHobbies
            results_hobs = OVCHobbies.objects.filter(case_id=id)
            results_hob = []
            for result_hobs in results_hobs:
                result_hobs_ = str(result_hobs.hobby)
                results_hob.append(result_hobs_)

            ovcccats = OVCCaseCategory.objects.filter(case_id=id)

            """ Retrieve Referrals/Interventions/CaseCategories """
            jsonData = []
            resultsets = []
            case_grouping_ids = []

            # Get case_grouping_ids[]
            for ovcccat in ovcccats:
                case_grouping_id = str(ovcccat.case_grouping_id)
                if not case_grouping_id in case_grouping_ids:
                    case_grouping_ids.append(str(case_grouping_id))

            # Get Case Categories/Interventions/Referrals
            ovcccats2 = None
            ovcintvs = None
            for case_grouping_id in case_grouping_ids:
                ovcccats2 = OVCCaseCategory.objects.filter(
                    case_grouping_id=case_grouping_id)
                ovcintvs = OVCInterventions.objects.filter(
                    case_grouping_id=case_grouping_id)
                ovcrefs = OVCReferral.objects.filter(
                    case_grouping_id=case_grouping_id)

                for ovcccat in ovcccats2:
                    jsonData.append({'case_category': ovcccat.case_category,
                                     'date_of_event': ovcccat.date_of_event,
                                     'case_grouping_id': str(ovcccat.case_grouping_id),
                                     'ovcintvs': ovcintvs,
                                     'ovcrefs': ovcrefs
                                     })
            resultsets.append(jsonData)

            # Manipulate Dates
            """
            date_case_opened = None
            if results_case.date_case_opened:
                the_date1 = convert_date(
                    str(results_case.date_case_opened), '%Y-%m-%d')
                date_case_opened = the_date1.strftime('%d-%b-%Y')
            """

            # Get Form Instance
            form = OVC_FT3hForm({'household_economics': results.household_economic_status,
                                 'family_status': results.family_status_id,
                                 'friends': results_frnd,
                                 'hobbies': results_hob,
                                 'mental_condition': results_med.mental_condition,
                                 'physical_condition': results_med.physical_condition,
                                 'other_condition': results_med.other_condition,
                                 'serial_number': results_case.case_serial,
                                 'perpetrator_first_name': results_case.perpetrator_first_name,
                                 'perpetrator_other_names': results_case.perpetrator_other_names,
                                 'perpetrator_surname': results_case.perpetrator_surname,
                                 'perpetrator_relationship': results_case.perpetrator_relationship_type,
                                 'place_of_event': results_case.place_of_event,
                                 'case_nature': results_case.case_nature,
                                 'risk_level': results_case.risk_level,
                                 'case_reporter_first_name': results_case.case_reporter_first_name,
                                 'case_reporter_other_names': results_case.case_reporter_other_names,
                                 'case_reporter_surname': results_case.case_reporter_surname,
                                 'case_reporter_contacts': results_case.case_reporter_contacts,
                                 'case_reporter_relationship_to_child': results_case.case_reporter_relationship_to_child,
                                 'date_case_opened': results_case.date_case_opened,
                                 'case_remarks': results_case.case_remarks
                                 })

            # Get PersonId/Init Data
            f = FormsAuditTrail.objects.get(form_id=id)
            person_id = int(f.person_id)
            init_data = RegPerson.objects.get(pk=person_id)
            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)

            return render(request, 'forms/edit_case_record_sheet.html',
                          {'form': form,
                           'init_data': init_data,
                           'vals': vals,
                           'resultsets': resultsets})
    except Exception, e:
        msg = 'An error occured trying to Edit OVCCaseRecord - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(forms_registry))

    msg = 'Update succesfull.'
    messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(forms_registry))


def view_case_record_sheet(request, id):
    try:
        """Get Initial Data"""
        f = FormsAuditTrail.objects.get(form_id=id)
        person_id = int(f.person_id)
        init_data = RegPerson.objects.filter(pk=person_id)
        check_fields = ['sex_id',
                        'family_status_id',
                        'household_economic_status',
                        'mental_condition_id',
                        'physical_condition_id',
                        'other_condition_id',
                        'case_nature_id',
                        'relationship_type_id',
                        'event_place_id',
                        'risk_level_id',
                        'referral_destination_id',
                        'intervention_id',
                        'case_category_id',
                        'core_item_id',
                        'case_reporter_relationship_to_child']
        vals = get_dict(field_name=check_fields)

        ovcd = OVCDetails.objects.get(case_id=id)
        ovcmed = OVCMedical.objects.get(case_id=id)
        ovcfrnds = OVCFriends.objects.filter(case_id=id)
        ovchobs = OVCHobbies.objects.filter(case_id=id)
        ovcneeds = OVCNeeds.objects.filter(case_id=id)
        ovccr = OVCCaseRecord.objects.get(case_id=id)
        ovcccats = OVCCaseCategory.objects.filter(case_id=id)

        """ Retrieve Referrals/Interventions/CaseCategories """
        jsonData = []
        resultsets = []
        case_grouping_ids = []

        # Get case_grouping_ids[]
        for ovcccat in ovcccats:
            case_grouping_id = str(ovcccat.case_grouping_id)
            if not case_grouping_id in case_grouping_ids:
                case_grouping_ids.append(str(case_grouping_id))

        # Get Case Categories/Interventions/Referrals
        ovcccats2 = None
        ovcintvs = None
        for case_grouping_id in case_grouping_ids:
            ovcccats2 = OVCCaseCategory.objects.filter(
                case_grouping_id=case_grouping_id)
            ovcintvs = OVCInterventions.objects.filter(
                case_grouping_id=case_grouping_id)
            ovcrefs = OVCReferral.objects.filter(
                case_grouping_id=case_grouping_id)

            for ovcccat in ovcccats2:
                jsonData.append({'case_category': ovcccat.case_category,
                                 'date_of_event': ovcccat.date_of_event,
                                 'case_grouping_id': str(ovcccat.case_grouping_id),
                                 'ovcintvs': ovcintvs,
                                 'ovcrefs': ovcrefs
                                 })
        resultsets.append(jsonData)

        return render(request,
                      'forms/view_case_record_sheet.html',
                      {'init_data': init_data,
                       'vals': vals,
                       'ovcd': ovcd,
                       'ovcmed': ovcmed,
                       'ovcfrnds': ovcfrnds,
                       'ovchobs': ovchobs,
                       'ovcneeds': ovcneeds,
                       'ovccr': ovccr,
                       'resultsets': resultsets
                       })
    except Exception, e:
        msg = 'An error occured trying to View OVCCaseRecord - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(forms_registry))


def delete_case_record_sheet(request, id):
    now = timezone.now()
    try:
        # OVCDetails
        ovcd = OVCDetails.objects.get(case_id=id)
        ovcd.is_void = True
        ovcd.timestamp_updated = now
        ovcd.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCMedical
        ovcmed = OVCMedical.objects.get(case_id=id)
        ovcmed.is_void = True
        ovcmed.timestamp_updated = now
        ovcmed.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCCaseRecord
        ovccr = OVCCaseRecord.objects.get(case_id=id)
        ovccr.is_void = True
        ovccr.timestamp_updated = now
        ovccr.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCCaseCategory
        ovcccats = OVCCaseCategory.objects.filter(case_id=id)
        for ovccat in ovcccats:
            ovccat.is_void = True
            ovccat.timestamp_updated = now
            ovccat.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCInterventions
        ovcintv = OVCInterventions.objects.filter(case_id=id)
        for ovcint in ovcintv:
            ovcint.is_void = True
            ovcint.timestamp_updated = now
            ovcint.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCReferral
        ovcrs = OVCReferral.objects.filter(case_id=id)
        for ovcr in ovcrs:
            ovcr.is_void = True
            ovcr.timestamp_updated = now
            ovcr.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCHobbies
        ovchobs = OVCHobbies.objects.filter(case_id=id)
        for ovchob in ovchobs:
            ovchob.is_void = True
            ovchob.timestamp_updated = now
            ovchob.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCNeeds
        ovcneeds = OVCNeeds.objects.filter(case_id=id)
        for ovcneed in ovcneeds:
            ovcneed.is_void = True
            ovcneed.timestamp_updated = now
            ovcneed.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCFriends
        ovcfrnds = OVCFriends.objects.filter(case_id=id)
        for ovcfrnd in ovcfrnds:
            ovcfrnd.is_void = True
            ovcfrnd.timestamp_updated = now
            ovcfrnd.save(update_fields=['is_void', 'timestamp_updated'])

        # FormsAuditTrail
        f = FormsAuditTrail.objects.get(form_id=id)
        f.is_void = True
        f.timestamp_updated = now
        f.save(update_fields=['is_void', 'timestamp_updated'])

    except Exception, e:
        msg = 'Form delete error (%s).' % str(e)
        messages.add_message(request, messages.INFO, msg)

    msg = 'Form delete succesfull (%s).' % id
    messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(forms_registry))


def case_record_sheet(request, id):
    '''
    Some default page for forms home page
    '''

    now = timezone.now()
    msg = ''
    try:
        if request.method == 'POST':
            form = OVC_FT3hForm(data=request.POST)

            # OVC_Case UUID()
            form_id = request.POST.get('case_id')
            #case_category_id = request.POST.get('case_category_id')

            # OVC_Reporting
            self_reporter = request.POST.get('self_reporter')
            case_reporter_first_name = request.POST.get(
                'case_reporter_first_name')
            case_reporter_other_names = request.POST.get(
                'case_reporter_other_names')
            case_reporter_surname = request.POST.get('case_reporter_surname')
            case_reporter_relationship_to_child = request.POST.get(
                'case_reporter_relationship_to_child')

            if(self_reporter):
                case_reporter_first_name = 'SELF-REPORTER'
                case_reporter_other_names = 'SELF-REPORTER'
                case_reporter_surname = 'SELF-REPORTER'
                case_reporter_relationship_to_child = 'NONE'

            case_reporter_contacts = request.POST.get('case_reporter_contacts')
            date_case_opened = request.POST.get('date_case_opened')
            if date_case_opened:
                date_case_opened = convert_date(date_case_opened)

            # OVC_Details
            person = request.POST.get('person')
            household_economic_status = request.POST.get('household_economics')
            family_status = request.POST.get('family_status')
            hobbies = request.POST.get('hobbies')
            friends = request.POST.get('friends')

            # OVC_Medical
            mental_condition = request.POST.get('mental_condition')
            physical_condition = request.POST.get('physical_condition')
            other_condition = request.POST.get('other_condition')

            # OVC_CaseRecord
            serial_number = request.POST.get('serial_number')
            perpetrator_first_name = request.POST.get('perpetrator_first_name')
            perpetrator_other_names = request.POST.get(
                'perpetrator_other_names')
            perpetrator_surname = request.POST.get('perpetrator_surname')
            perpetrator_relationship = request.POST.get(
                'perpetrator_relationship')
            place_of_event = request.POST.get('place_of_event')
            case_nature = request.POST.get('case_nature')
            risk_level = request.POST.get('risk_level')
            immediate_needs = request.POST.get('immediate_needs')
            future_needs = request.POST.get('future_needs')
            case_remarks = request.POST.get('case_remarks')

            # OVCCaseRecord
            try:
                OVCCaseRecord(
                    case_id=form_id,
                    case_serial=serial_number,
                    # date_of_event=date_of_event,
                    place_of_event=place_of_event,
                    perpetrator_first_name=perpetrator_first_name,
                    perpetrator_other_names=perpetrator_other_names,
                    perpetrator_surname=perpetrator_surname,
                    perpetrator_relationship_type=perpetrator_relationship,
                    # case_category=case_category,
                    case_reporter_first_name=case_reporter_first_name,
                    case_reporter_other_names=case_reporter_other_names,
                    case_reporter_surname=case_reporter_surname,
                    case_reporter_contacts=case_reporter_contacts,
                    case_reporter_relationship_to_child=case_reporter_relationship_to_child,
                    date_case_opened=date_case_opened,
                    case_nature=case_nature,
                    risk_level=risk_level,
                    # intervention=intervention,
                    case_remarks=case_remarks,
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving case record info : %s' % str(
                        e)
                messages.add_message(request, messages.INFO, msg)

            # OVCCaseCategory / OVCInterventions / OVCReferral
            try:
                for jsonObject in jsonObjectArray:
                    case_grouping_id = new_guid_32(),
                    case_category = jsonObject['case_category']
                    interventions = jsonObject['interventions']
                    refferals_to = jsonObject['refferals_to']
                    date_of_event = jsonObject['date_of_event']
                    if date_of_event:
                        date_of_event = convert_date(date_of_event)

                    for i, category in enumerate(case_category):
                        OVCCaseCategory(
                            case_category_id=new_guid_32(),
                            case_id=OVCCaseRecord.objects.get(pk=form_id),
                            case_category=category,
                            date_of_event=date_of_event,
                            case_grouping_id=case_grouping_id,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))
                        ).save()

                    for i, intervention in enumerate(interventions):
                        OVCInterventions(
                            inteventions_id=new_guid_32(),
                            intervention=intervention,
                            case_grouping_id=case_grouping_id,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()

                    for i, refferal_to in enumerate(refferals_to):
                        OVCReferral(
                            refferal_id=new_guid_32(),
                            refferal_to=refferal_to,
                            case_grouping_id=case_grouping_id,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving case category info : %s' % str(
                        e)
                messages.add_message(request, messages.INFO, msg)

            # OVCDetails
            try:
                OVCDetails(
                    case_id=OVCCaseRecord.objects.get(pk=form_id),
                    family_status_id=family_status,
                    household_economic_status=household_economic_status,
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                # print 'Error occured when saving OVCDetails : %s' % str(e)
                msg = msg + \
                    '\nError occured when saving OVCDetails : %s' % str(e)
                messages.add_message(request, messages.INFO, msg)

            # OVCHobbies
            try:
                if hobbies:
                    hobbies = str(hobbies).split(",")
                    # print 'Hobbies --------- %s' %hobbies
                    for hobby in hobbies:
                        OVCHobbies(
                            case_id=OVCCaseRecord.objects.get(pk=form_id),
                            hobby=hobby.upper(),
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + '\nError occured when saving hobbies : %s' % str(e)
                messages.add_message(request, messages.INFO, msg)

            # OVCFriends
            # print 'OVCFriends: %s' %friends
            try:
                if friends:
                    friends = str(friends).split(",")
                    # print 'OVCFriends split(","): %s' %friends
                    for i, friend in enumerate(friends):
                        names = (friends[i]).split()
                        # print 'OVCFriends split(",")[names]: %s' %names
                        if(len(names) == 1):
                            ffname = names[0]
                            foname = 'XXXX'
                            fsname = 'XXXX'
                        if(len(names) == 2):
                            ffname = names[0]
                            foname = names[1]
                            fsname = 'XXXX'
                        if(len(names) == 3):
                            ffname = names[0]
                            foname = names[1]
                            fsname = names[2]
                        OVCFriends(
                            case_id=OVCCaseRecord.objects.get(pk=form_id),
                            friend_firstname=ffname.upper(),
                            friend_other_names=foname.upper(),
                            friend_surname=fsname.upper(),
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + '\nError occured when saving friends : %s' % str(e)
                messages.add_message(request, messages.INFO, msg)

            # OVCMedical
            try:
                OVCMedical(
                    case_id=OVCCaseRecord.objects.get(pk=form_id),
                    mental_condition=mental_condition,
                    physical_condition=physical_condition,
                    other_condition=other_condition,
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving medical info : %s' % str(e)
                messages.add_message(request, messages.INFO, msg)

            # OVCNeeds
            if immediate_needs:
                need_type = 'IMMEDIATE'
                immediate_needs = str(immediate_needs).split(",")
                for immediate_need in immediate_needs:
                    OVCNeeds(
                        case_id=OVCCaseRecord.objects.get(pk=form_id),
                        need_description=immediate_need.upper(),
                        need_type=need_type,
                        timestamp_created=now,
                        person=RegPerson.objects.get(pk=int(person))
                    ).save()
            if future_needs:
                need_type = 'FUTURE'
                future_needs = str(future_needs).split(",")
                for future_need in future_needs:
                    OVCNeeds(
                        case_id=OVCCaseRecord.objects.get(pk=form_id),
                        need_description=future_need.upper(),
                        need_type=need_type,
                        timestamp_created=now,
                        person=RegPerson.objects.get(pk=int(person))
                    ).save()

            # FormsAuditTrail
            try:
                FormsAuditTrail(
                    form_id=form_id,
                    form_type_id='FT3h',
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving FormsAuditTrail : %s' % str(e)
                messages.add_message(request, messages.INFO, msg)
        else:
            # Generate UUIDs()
            case_id = new_guid_32()  # uuid_1
            case_category_id = new_guid_32()  # uuid_2

            init_data = RegPerson.objects.filter(pk=id)
            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)
            form = OVC_FT3hForm({
                'self_reporter': 'on',
                'case_id': case_id,
                'case_category_id': case_category_id})
            return render(request, 'forms/case_record_sheet.html', {'form': form,
                                                                    #'uuid': uuid,
                                                                    'init_data': init_data,
                                                                    'vals': vals})

    except Exception, e:
        msg = msg + 'Form  save error: (%s)' % (str(e))
        messages.add_message(request, messages.INFO, msg)

        """
        # Delete Related on Exception e
        if OVCDetails.objects.filter(case_id=form_id):
            OVCDetails.objects.filter(case_id=form_id).delete()
        if OVCReferral.objects.filter(case_id=form_id):
            OVCReferral.objects.filter(case_id=form_id).delete()
        if OVCHobbies.objects.filter(case_id=form_id):
            OVCHobbies.objects.filter(case_id=form_id).delete()
        if OVCFriends.objects.filter(case_id=form_id):
            OVCFriends.objects.filter(case_id=form_id).delete()
        if OVCMedical.objects.filter(case_id=form_id):
            OVCMedical.objects.filter(case_id=form_id).delete()
        if OVCCaseRecord.objects.filter(case_id=form_id):
            OVCCaseRecord.objects.filter(case_id=form_id).delete()
        if OVCCaseCategory.objects.filter(case_id=form_id):
            OVCCaseCategory.objects.filter(case_id=form_id).delete()
        if OVCInterventions.objects.filter(case_id=form_id):
            OVCInterventions.objects.filter(case_id=form_id).delete()
        if OVCNeeds.objects.filter(case_id=form_id):
            OVCNeeds.objects.filter(case_id=form_id).delete()
        if FormsAuditTrail.objects.filter(form_id=form_id):
            FormsAuditTrail.objects.filter(form_id=form_id).delete()
        """

    msg = msg + '\nForm save succesfull.'
    messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(ovc_search))


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
            form = OVCSearchForm(
                data=request.POST, initial={'person_type': 'TBVC'})
            check_fields = ['sex_id', 'cadre_type_id', 'person_type_id',
                            'relationship_type_id', 'identifier_type_id']
            vals = get_dict(field_name=check_fields)

            person_type = request.POST.get('person_type')
            search_string = request.POST.get('search_name')
            search_criteria = request.POST.get('search_criteria')

            # Preselect PersonType selection mandatory
            # if person_type:
            wfc_type = 'TBVC'

            # Filter Location Searches
            if search_criteria == 'ORG':
                search_wfc_by_org_unit = False
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
                                    person_org.org_unit_id)

                            result.pgeolocs = pgeolocs_
                            result.porgs = porgs_

            msg = 'Showing results for (%s)' % search_string
            messages.add_message(request, messages.INFO, msg)
            return render(request, 'forms/forms_index.html',
                          {'form': form, 'resultsets': resultsets, 'vals': vals, 'person_type': person_type})
        except Exception, e:
            msg = 'OVC search error - %s' % (str(e))
            messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(ovc_search))
    else:
        form = OVCSearchForm(initial={'search_criteria': 'NAME'})
        return render(request, 'forms/forms_index.html',
                      {'form': form})


def case_events(request, id):
    check_fields = ['intervention_id',
                    'case_nature_id',
                    'risk_level_id',
                    'case_category_id',
                    'core_item_id',
                    'event_place_id']
    vals = get_dict(field_name=check_fields)

    resultsets = set()

    # FormsAuditTrail
    audit_trail = FormsAuditTrail.objects.filter(
        form_id=id, is_void=False)
    resultsets.add(audit_trail)

    # OVCCaseEvents
    c_events = OVCCaseEvents.objects.filter(
        case_id=id, is_void=False).order_by('-timestamp_created')

    # OVCCaseRecord
    ovccr = OVCCaseRecord.objects.filter(case_id=id, is_void=False)

    # OVCCaseCategory
    ovcccats = OVCCaseCategory.objects.filter(case_id=id, is_void=False)

    # Get case_grouping_ids[]
    case_grouping_ids = []
    for ovcccat in ovcccats:
        case_grouping_id = str(ovcccat.case_grouping_id)
        if not case_grouping_id in case_grouping_ids:
            case_grouping_ids.append(str(case_grouping_id))

    # OVCReferral
    ovcrefs = OVCReferral.objects.filter(
        case_grouping_id__in=case_grouping_ids, is_void=False)

    # OVCInterventions
    ovcintvs = OVCInterventions.objects.filter(
        case_grouping_id__in=case_grouping_ids, is_void=False)

    # Generate Resultsets Object
    for resultset in resultsets:
        for res in resultset:
            if ovccr:
                res.c_record = ovccr
            if c_events:
                res.c_evnts = c_events
            if ovcccats:
                res.c_cats = ovcccats
            if ovcrefs:
                res.c_refs = ovcrefs
            if ovcintvs:
                res.c_intvs = ovcintvs

    form = OVC_CaseEventForm(
        initial={'case_id': id, })
    return render(request, 'forms/case_events.html',
                  {
                      'form': form, 'vals': vals,
                      'resultsets': resultsets
                  })


def save_encounter(request):
    now = timezone.now()
    # generate unique CE_id
    ce_rand = random.randint(100000, 999999)
    case_event_id = case_event_id_generator(ce_rand)
    user_id = 0

    try:
        if request.method == 'POST':

            # Get app_user
            username = request.user.get_username()
            app_user = AppUser.objects.get(username=username)
            user_id = app_user.id

            case_id = request.POST.get('case_id')
            date_of_encounter_event = request.POST.get(
                'date_of_encounter_event')
            if date_of_encounter_event:
                date_of_encounter_event = convert_date(date_of_encounter_event)
            encounter_notes = request.POST.get('encounter_notes')
            services_provided = request.POST.getlist('services_provided')
            #refferals_completed = request.POST.getlist('refferals_completed')

            # OVCCaseEvents
            OVCCaseEvents(
                case_event_id=case_event_id,
                case_event_type_id='SERVICES',
                date_of_event=date_of_encounter_event,
                case_event_details='case_event_details',
                case_event_notes=encounter_notes,
                case_id=OVCCaseRecord.objects.get(pk=case_id),
                app_user=AppUser.objects.get(pk=user_id)
            ).save()

            # OVCCaseEventServices
            for i, service_provided in enumerate(services_provided):
                service_provided = service_provided.split(',')
                for service in service_provided:
                    OVCCaseEventServices(
                        service_provided=str(service),
                        case_event_id=OVCCaseEvents.objects.get(pk=case_event_id)).save()

        else:
            print 'Not POST'
    except Exception, e:
        print 'Encounter Save Error: %s' % str(e)
    # return HttpResponseRedirect(reverse(ovc_search))
    return HttpResponse('Encounter Saved')


def view_encounter(request):
    resultsets = set()
    ovc_events = None
    ovc_services = []
    jsonCeData = []
    jsonSvcsData = []

    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            ovc_events_svcs = OVCCaseEventServices.objects.filter(
                case_event_id=case_event_id)
            for ovc_events_svc in ovc_events_svcs:
                ovc_services.append(str(ovc_events_svc.service_provided))

            ovc_events = OVCCaseEvents.objects.filter(
                case_event_id=case_event_id)
            for ovc_event in ovc_events:
                jsonCeData.append({'case_event_type_id': str(ovc_event.case_event_type_id),
                                   'date_of_event': str(ovc_event.date_of_event),
                                   'case_event_notes': str(ovc_event.case_event_notes),
                                   'ovc_services': ovc_services
                                   })

            # test
            # combined = chain(jsonCeData, jsonSvcsData)
            # json_combined = serializers.serialize('json', combined)
            # print 'json_combined %s' %json_combined
        else:
            print 'Not POST'
    except Exception, e:
        print 'Encounter View Error: %s' % str(e)
    # return HttpResponse(jsonCeData, mimetype='text/json')
    return JsonResponse(jsonCeData, content_type='application/json',
                        safe=False)


def edit_encounter(request):
    now = timezone.now()

    try:
        if request.method == 'POST':
            case_id = request.POST.get('case_id')
            case_event_id = request.POST.get('case_event_id')
            date_of_encounter_event = request.POST.get(
                'date_of_encounter_event')
            if date_of_encounter_event:
                date_of_encounter_event = convert_date(date_of_encounter_event)
            encounter_notes = request.POST.get('encounter_notes')
            services_provided = request.POST.getlist('services_provided')
            #refferals_completed = request.POST.getlist('refferals_completed')

            print 'case_event_id ---- %s' % case_event_id
            # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            ovc_ce.date_of_event = date_of_encounter_event
            ovc_ce.case_event_notes = encounter_notes
            ovc_ce.timestamp_updated = now
            ovc_ce.save(
                update_fields=['date_of_event', 'case_event_notes', 'timestamp_updated'])

            # Update Services Provided
            existing_services_provided = []
            ovc_services = OVCCaseEventServices.objects.filter(
                case_event_id=case_event_id)
            for ovc_service in ovc_services:
                existing_services_provided.append(
                    str(ovc_service.service_provided))

            """ Cater for Unchecked yet Pre-existed """
            for i, eservice in enumerate(existing_services_provided):
                if not(str(eservice) in services_provided):
                    OVCCaseEventServices.objects.filter(
                        case_event_id=case_event_id, service_provided=eservice).delete()

            """ Cater for new selected service_provided """
            for i, service_provided in enumerate(services_provided):
                if not (str(service_provided) in existing_services_provided):
                    service_provided = service_provided.split(',')
                    for service in service_provided:
                        OVCCaseEventServices(
                            service_provided=service,
                            case_event_id=OVCCaseEvents.objects.get(pk=case_event_id)).save()
        else:
            print 'Not POST'
    except Exception, e:
        print 'Encounter Edit Error: %s' % str(e)
    # return HttpResponseRedirect(reverse(ovc_search))
    return HttpResponse('Encounter Updated')


def delete_encounter(request):
    now = timezone.now()

    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            ovc_ce.is_void = True
            ovc_ce.save(update_fields=['is_void'])

            # Delete/Void Services Provided
            ovc_services = OVCCaseEventServices.objects.filter(
                case_event_id=case_event_id)
            for ovc_service in ovc_services:
                ovc_service.is_void = True
                ovc_service.save(update_fields=['is_void'])
        else:
            print 'Not POST'
    except Exception, e:
        print 'Encounter Delete Error: %s' % str(e)
    # return HttpResponseRedirect(reverse(ovc_search))
    return HttpResponse('Encounter Deleted')


def save_court(request):
    try:
        if request.method == 'POST':
            now = timezone.now()

            # Get app_user
            username = request.user.get_username()
            app_user = AppUser.objects.get(username=username)
            user_id = app_user.id

            # generate unique CE_id
            ce_rand = random.randint(100000, 999999)
            case_event_id = case_event_id_generator(ce_rand)

            case_id = request.POST.get('case_id')
            date_of_court_event = request.POST.get('date_of_court_event')
            if date_of_court_event:
                date_of_court_event = convert_date(date_of_court_event)
            court_notes = request.POST.get('court_notes')
            court_orders = request.POST.getlist('court_orders')

            # OVCCaseEvents
            OVCCaseEvents(
                case_event_id=case_event_id,
                case_event_type_id='COURT',
                date_of_event=date_of_court_event,
                case_event_details='case_event_details',
                case_event_notes=court_notes,
                case_id=OVCCaseRecord.objects.get(pk=case_id),
                app_user=AppUser.objects.get(pk=user_id)
            ).save()

            # OVCCaseEventServices
            for i, court_order in enumerate(court_orders):
                court_order = court_order.split(',')
                for order in court_order:
                    OVCCaseEventCourt(
                        court_order=order,
                        case_event_id=OVCCaseEvents.objects.get(pk=case_event_id)).save()
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Session Save Error: %s' % str(e)
    return HttpResponse('Court Session Saved')


def view_court(request):
    ovc_court_orders = []
    jsonCourtData = []
    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            ovc_court_events = OVCCaseEventCourt.objects.filter(
                case_event_id=case_event_id)
            for ovc_court_event in ovc_court_events:
                ovc_court_orders.append(str(ovc_court_event.court_order))

            ovc_events = OVCCaseEvents.objects.filter(
                case_event_id=case_event_id)
            for ovc_event in ovc_events:
                jsonCourtData.append({'case_event_type_id': str(ovc_event.case_event_type_id),
                                      'date_of_event': str(ovc_event.date_of_event),
                                      'case_event_notes': str(ovc_event.case_event_notes),
                                      'ovc_court_orders': ovc_court_orders
                                      })
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Session View Error: %s' % str(e)

    return JsonResponse(jsonCourtData, content_type='application/json',
                        safe=False)


def edit_court(request):
    now = timezone.now()

    try:
        if request.method == 'POST':
            case_id = request.POST.get('case_id')
            case_event_id = request.POST.get('case_event_id')
            date_of_court_event = request.POST.get(
                'date_of_court_event')
            if date_of_court_event:
                date_of_court_event = convert_date(date_of_court_event)
            court_notes = request.POST.get('court_notes')
            court_orders = request.POST.getlist('court_orders')
            #refferals_completed = request.POST.getlist('refferals_completed')

            # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            ovc_ce.date_of_event = date_of_court_event
            ovc_ce.case_event_notes = court_notes
            ovc_ce.timestamp_updated = now
            ovc_ce.save(
                update_fields=['date_of_event', 'case_event_notes', 'timestamp_updated'])

            # Update Court Orders
            existing_court_orders = []
            ovc_court_orders = OVCCaseEventCourt.objects.filter(
                case_event_id=case_event_id)
            for ovc_court_order in ovc_court_orders:
                existing_court_orders.append(str(ovc_court_order.court_order))

            """ Cater for Unchecked yet Pre-existed """
            for i, ecourt_order in enumerate(existing_court_orders):
                if not(str(ecourt_order) in court_orders):
                    OVCCaseEventCourt.objects.filter(
                        case_event_id=case_event_id, court_order=ecourt_order).delete()

            """ Cater for new selected court orders """
            for i, court_order in enumerate(court_orders):
                if not (str(court_order) in existing_court_orders):
                    court_order = court_order.split(',')
                    for order in court_order:
                        OVCCaseEventCourt(
                            court_order=order,
                            case_event_id=OVCCaseEvents.objects.get(pk=case_event_id)).save()
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Sessions Edit Error: %s' % str(e)
    # return HttpResponseRedirect(reverse(ovc_search))
    return HttpResponse('Court Sessions Updated')


def delete_court(request):
    now = timezone.now()

    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            ovc_ce.is_void = True
            ovc_ce.save(update_fields=['is_void'])

            # Delete/Void Court Orders Provided
            ovc_court_orders = OVCCaseEventCourt.objects.filter(
                case_event_id=case_event_id)
            for ovc_court_order in ovc_court_orders:
                ovc_court_order.is_void = True
                ovc_court_order.save(update_fields=['is_void'])
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Orders Delete Error: %s' % str(e)
    # return HttpResponseRedirect(reverse(ovc_search))
    return HttpResponse('Court Orders Deleted')


def save_placement(request):
    try:
        if request.method == 'POST':
            now = timezone.now()

            # Get app_user
            username = request.user.get_username()
            app_user = AppUser.objects.get(username=username)
            user_id = app_user.id

            # generate unique CE_id
            ce_rand = random.randint(100000, 999999)
            case_event_id = case_event_id_generator(ce_rand)

            case_id = request.POST.get('case_id')
            date_of_placement_event = request.POST.get(
                'date_of_placement_event')
            if date_of_placement_event:
                date_of_placement_event = convert_date(date_of_placement_event)
            placement_notes = request.POST.get('placement_notes')
            residential_institution = request.POST.get(
                'residential_institution')
            current_residential_status = request.POST.get(
                'current_residential_status')
            has_court_committal_order = request.POST.get(
                'has_court_committal_order')
            free_for_adoption = request.POST.get('free_for_adoption')
            admission_date = request.POST.get('admission_date')
            if admission_date:
                admission_date = convert_date(admission_date)

            departure_date = request.POST.get('departure_date')
            if departure_date:
                departure_date = convert_date(departure_date)

            # OVCCaseEvents
            OVCCaseEvents(
                case_event_id=case_event_id,
                case_event_type_id='PLACEMENT',
                date_of_event=date_of_placement_event,
                case_event_details='case_event_details',
                case_event_notes=placement_notes,
                case_id=OVCCaseRecord.objects.get(pk=case_id),
                app_user=AppUser.objects.get(pk=user_id)
            ).save()

            # OVCCaseEventPlacement
            OVCCaseEventPlacement(
                residential_institution=RegOrgUnit.objects.get(
                    pk=int(residential_institution)),
                current_residential_status=current_residential_status,
                has_court_committal_order=has_court_committal_order,
                free_for_adoption=free_for_adoption,
                admission_date=admission_date.date(),
                # departure_date=departure_date,
                case_event_id=OVCCaseEvents.objects.get(pk=case_event_id)
            ).save()

        else:
            print 'Not POST'
    except Exception, e:
        print 'Residential Placement Save Error: %s' % str(e)
    return HttpResponse('Residential Placement Saved')


def view_placement(request):
    ovc_placements = []
    jsonPlacementData = []
    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            ovc_placement_events = OVCCaseEventPlacement.objects.filter(
                case_event_id=case_event_id)
            for ovc_placement_event in ovc_placement_events:
                #the_departure_date = convert_date(ovc_placement_event.departure_date, '%Y-%m-%d')
                #departure_date = the_departure_date.strftime('%d-%b-%Y')
                ovc_placements.append(
                    str(ovc_placement_event.residential_institution))  # 0
                ovc_placements.append(
                    str(ovc_placement_event.current_residential_status))  # 1
                ovc_placements.append(
                    str(ovc_placement_event.has_court_committal_order))  # 2
                ovc_placements.append(
                    str(ovc_placement_event.free_for_adoption))  # 3
                ovc_placements.append(
                    str(ovc_placement_event.admission_date))  # 4
                ovc_placements.append(
                    str(ovc_placement_event.departure_date))  # 5
                ovc_placements.append(
                    str(ovc_placement_event.case_event_id))  # 6

                print 'ovc_placements: %s' % ovc_placements

            ovc_events = OVCCaseEvents.objects.filter(
                case_event_id=case_event_id)
            for ovc_event in ovc_events:
                jsonPlacementData.append({'case_event_type_id': str(ovc_event.case_event_type_id),
                                          'date_of_event': str(ovc_event.date_of_event),
                                          'case_event_notes': str(ovc_event.case_event_notes),
                                          'ovc_placements': ovc_placements
                                          })
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Session View Error: %s' % str(e)

    return JsonResponse(jsonPlacementData, content_type='application/json',
                        safe=False)


def edit_placement(request):
    now = timezone.now()
    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('case_event_id')
            case_id = request.POST.get('case_id')
            date_of_placement_event = request.POST.get(
                'date_of_placement_event')
            if date_of_placement_event:
                date_of_placement_event = convert_date(date_of_placement_event)
            placement_notes = request.POST.get('placement_notes')
            residential_institution = request.POST.get(
                'residential_institution')
            current_residential_status = request.POST.get(
                'current_residential_status')
            has_court_committal_order = request.POST.get(
                'has_court_committal_order')
            free_for_adoption = request.POST.get('free_for_adoption')
            admission_date = request.POST.get('admission_date')
            if admission_date:
                admission_date = convert_date(admission_date)
            departure_date = request.POST.get('departure_date')
            if departure_date:
                departure_date = convert_date(departure_date)

             # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            ovc_ce.date_of_event = date_of_placement_event
            ovc_ce.case_event_notes = placement_notes
            ovc_ce.timestamp_updated = now
            ovc_ce.save(
                update_fields=['date_of_event', 'case_event_notes', 'timestamp_updated'])

            # Update OVCCaseEventPlacement
            ovc_plcmnt = OVCCaseEventPlacement.objects.get(
                case_event_id=case_event_id)
            ovc_plcmnt.residential_institution = residential_institution
            ovc_plcmnt.current_residential_status = current_residential_status
            ovc_plcmnt.has_court_committal_order = has_court_committal_order
            ovc_plcmnt.free_for_adoption = free_for_adoption
            #ovc_plcmnt.admission_date = admission_date
            #ovc_plcmnt.departure_date = departure_date
            ovc_plcmnt.save(update_fields=['residential_institution',
                                           'current_residential_status',
                                           'has_court_committal_order',
                                           'free_for_adoption',
                                           'admission_date',
                                           'departure_date'])
        else:
            print 'Not POST'
    except Exception, e:
        print 'Residential Placement Edit Error: %s' % str(e)
    return HttpResponse('Residential Placement Updated')


def delete_placement(request):
    now = timezone.now()

    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            ovc_ce.is_void = True
            ovc_ce.save(update_fields=['is_void'])

            # Delete/Void Residential Placement
            ovc_plcmnts = OVCCaseEventPlacement.objects.filter(
                case_event_id=case_event_id)
            for ovc_plcmnt in ovc_plcmnts:
                ovc_plcmnt.is_void = True
                ovc_plcmnt.save(update_fields=['is_void'])
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Orders Delete Error: %s' % str(e)
    # return HttpResponseRedirect(reverse(ovc_search))
    return HttpResponse('Court Orders Deleted')


def manage_refferal(request):
    try:
        if request.method == 'POST':
            now = timezone.now()
            # generate unique CE_id
            ce_rand = random.randint(100000, 999999)
            case_event_id = case_event_id_generator(ce_rand)

            case_id = request.POST.get('case_id')
            refferals_made = request.POST.getlist('refferals_made')
            jsonObject = request.POST.get('TableData')
            data = json.loads(jsonObject)
            for d in data:
                # Remove nulls
                if d:
                    refferal_id = d['id']
                    refferal_status = d['status']
                    refferal_date = d['date_of_referral_event']
                    if refferal_date:
                        refferal_date = convert_date(refferal_date)

                    ovcref = OVCReferral.objects.get(
                        case_id=case_id, id=refferal_id)
                    ovcref.refferal_status = refferal_status
                    ovcref.date_of_referral_event = refferal_date
                    ovcref.timestamp_updated = now
                    ovcref.save(
                        update_fields=['date_of_referral_event', 'refferal_status', 'timestamp_updated'])

            # OVCReferral (New)
            pkey = OVCCaseRecord.objects.get(case_id=case_id)
            for i, refferal_made in enumerate(refferals_made):
                if refferal_made:
                    refferal_made = refferal_made.split(',')
                    for refferal in refferal_made:
                        ovcref = OVCReferral.objects.filter(
                            case_id=case_id, refferal_to=refferal)
                        # If DoesNotEXist, save(), else DONothing
                        if not ovcref:
                            OVCReferral(
                                case_id=OVCCaseRecord.objects.get(pk=case_id),
                                # refferal_destination_type=refferal_destination_type,
                                refferal_to=refferal,
                                # refferal_reason=refferal_reason,
                                timestamp_created=now,
                                person=RegPerson.objects.get(pk=int(pkey.person_id))).save()
        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage Referral Error: %s' % str(e)
    return HttpResponse('Manage Referral Success')

# Append Dicts to jsonObjectArray


def manage_refferal001(request):
    try:
        if request.method == 'POST':
            jsonObject = request.POST.get('CaseManagementData')
            data = json.loads(jsonObject)
            jsonObjectArray.append(data)
        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage Referral001 Error: %s' % str(e)
    return HttpResponse('Manage Referral001 Success : List.Append()')

# Remove Dicts from jsonObjectArray


def manage_refferal002(request):
    try:
        if request.method == 'POST':
            index = int(request.POST.get('index'))
            jsonObjectArray.pop(index - 1)
        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage Referral002 Error: %s' % str(e)
    return HttpResponse('Manage Referral002 Success : List.Remove()')


def manage_refferal003(request):
    try:
        case_category_list = []
        date_of_event_list = []
        intervention_list = []
        referral_list = []
        jsonRefferalsData = []

        if request.method == 'POST':
            case_grouping_id = request.POST.get('span_case_grouping_id')

            ovcccats = OVCCaseCategory.objects.filter(
                case_grouping_id=case_grouping_id, is_void=False)
            ovcintvs = OVCInterventions.objects.filter(
                case_grouping_id=case_grouping_id, is_void=False)
            ovcrefs = OVCReferral.objects.filter(
                case_grouping_id=case_grouping_id, is_void=False)

            for ovcccat in ovcccats:
                case_category_list.append(str(ovcccat.case_category))
                date_of_event_list.append(str(ovcccat.date_of_event))
            for ovcintv in ovcintvs:
                intervention_list.append(str(ovcintv.intervention))
            for ovcref in ovcrefs:
                referral_list.append(str(ovcref.refferal_to))

            jsonRefferalsData.append({'case_category_list': case_category_list,
                                      'date_of_event_list': date_of_event_list,
                                      'intervention_list': intervention_list,
                                      'referral_list': referral_list})

        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage Referral003 Error: %s' % str(e)
    return JsonResponse(jsonRefferalsData, content_type='application/json',
                        safe=False)

def getJsonObject001(request):
    jsonCaseCategories = []
    case_categories = []
    case_grouping_ids = []

    try:
        if request.method == 'POST':
            case_id = request.POST.get('case_id')
            ovcccats = OVCCaseCategory.objects.filter(case_id=case_id)
            for ovcccat in ovcccats:
                jsonCaseCategories.append({'case_category_id': str(ovcccat.case_category_id),
                                           'case_category': translate(ovcccat.case_category)})
        else:
            print 'getJsonObject001 - Not a POST'
    except Exception, e:
        print 'getJsonObject001 Error: %s' % str(e)
    return JsonResponse(jsonCaseCategories, content_type='application/json',
                        safe=False)


def close_case(request):
    jsonClosureData = []
    try:
        if request.method == 'POST':
            now = timezone.now()
            case_id = request.POST.get('case_id')
            case_status = request.POST.get('case_status')
            # Awaiting Case Status
            if case_status == 'YES':
                case_status = 'ACTIVE'
            elif case_status == 'NO':
                case_status = 'INACTIVE'

            case_outcome_notes = request.POST.get('case_outcome_notes')
            date_of_case_closure = request.POST.get('date_of_case_closure')
            if date_of_case_closure:
                date_of_case_closure = convert_date(date_of_case_closure)

            ovccr_exist = OVCCaseRecord.objects.filter(
                case_id=case_id, case_status='INACTIVE')

            if not ovccr_exist:
                # OVCCaseClosure
                ovcc = OVCCaseClosure(
                    case_status=case_status,
                    case_outcome_notes=case_outcome_notes,
                    date_of_case_closure=date_of_case_closure,
                    case_id=OVCCaseRecord.objects.get(pk=case_id)
                )
                ovcc.save()

                if ovcc:
                    # OVCCaseRecord
                    ovccr = OVCCaseRecord.objects.get(pk=case_id)
                    ovccr.case_status = case_status
                    ovccr.save(update_fields=['case_status'])
                jsonClosureData.append(
                    {'closure_status': 'OPEN', 'case_status': case_status})
            else:
                # OVCCaseRecord
                ovccl = OVCCaseClosure.objects.get(case_id=case_id)
                ovccl.case_status = case_status
                ovccl.save(update_fields=['case_status'])

                if ovccl:
                    # OVCCaseRecord
                    ovccr = OVCCaseRecord.objects.get(pk=case_id)
                    ovccr.case_status = case_status
                    ovccr.save(update_fields=['case_status'])
                jsonClosureData.append(
                    {'closure_status': 'CLOSED', 'case_status': case_status})
        else:
            print 'Not a POST $'

    except Exception, e:
        print 'Case Close Error: %s' % str(e)
    return JsonResponse(jsonClosureData, content_type='application/json',
                        safe=False)
