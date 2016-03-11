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
    OVCSearchForm, ResidentialSearchForm, ResidentialFollowupForm, ResidentialForm, OVC_FT3hForm,
    SearchForm, OVC_CaseEventForm, DocumentsManager)
from cpovc_forms.models import (OVCDetails, OVCReferral, OVCHobbies, OVCFriends, OVCDocuments,
                                OVCMedical, OVCCaseRecord, OVCNeeds, OVCCaseCategory, OVCInterventions,
                                FormsAuditTrail, OVCCaseEvents, OVCCaseEventServices, OVCCaseEventCourt,
                                OVCPlacement, OVCPlacementFollowUp, OVCDischargeFollowUp, OVCEducationFollowUp,
                                OVCAdverseEventsFollowUp, OVCAdverseMedicalEventsFollowUp, OVCCaseClosure,
                                OVCCaseGeo, OVCMedicalSubconditions)
from cpovc_main.functions import (
    get_list_of_org_units, get_dict, get_vgeo_list, get_vorg_list, get_persons_list, form_id_generator,
    case_event_id_generator, convert_date, new_guid_32, beneficiary_id_generator, translate_geo, translate,
    translate_case)
from cpovc_registry.models import (
    RegOrgUnit, RegOrgUnitContact, RegPerson, RegPersonsOrgUnits, AppUser,
    RegPersonsTypes, RegPersonsGuardians, RegPersonsGeo, RegPersonsExternalIds)
from cpovc_main.models import (SetupList, SetupGeography)
from cpovc_auth.models import CPOVCUserRoleGeoOrg


jsonObjectArray = []  # Manage CaseCategorys
jsonObjectArrayServices = []  # Manage Encounters/Services

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


def usersubcounty_lookup(request):
    # For JSON lookup stuff on Case Geo Locs pages
    try:
        if request.method == 'POST':
            user_id = request.POST.get('user_id')

            jsonSubcountyResults = []
            subcounty_ids = []
            user_geolocs = CPOVCUserRoleGeoOrg.objects.filter(
                user_id=int(user_id))
            for user_geoloc in user_geolocs:
                subcounty_ids.append(int(user_geoloc.area.area_id))
            for subcounty_id in subcounty_ids:
                jsonSubcountyResults.append({'area_id': subcounty_id,
                                             'area_name': translate_geo(subcounty_id)})
    except Exception, e:
        raise e
    return JsonResponse(jsonSubcountyResults, content_type='application/json',
                        safe=False)


def userward_lookup(request):
    # For JSON lookup stuff on Case Geo Locs pages
    try:
        if request.method == 'POST':
            subcounty = request.POST.get('subcounty')

            jsonWardResults = []

            user_geolocs = SetupGeography.objects.filter(
                parent_area_id=int(subcounty))
            for user_geoloc in user_geolocs:
                jsonWardResults.append({'area_id': user_geoloc.area_id,
                                        'area_name': translate_geo(user_geoloc.area_id)})
    except Exception, e:
        raise e
    return JsonResponse(jsonWardResults, content_type='application/json',
                        safe=False)


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
                                msg = 'Showing results for %s Form (Filter Name - %s)' % (
                                    translate(form_type), form_owner.upper())
                                messages.add_message(
                                    request, messages.INFO, msg)
                    else:
                        msg = 'Search returned 0 results.Displaying all forms.'
                        messages.add_message(request, messages.INFO, msg)
            for f in tmp_result:
                resultsets.add(tmp_result)

            # print 'form_type ------------ %s' %form_type
            if form_type == 'FTRI':
                # print 'Do Your Work Here'
                for resultset in resultsets:
                    for result in resultset:
                         # Get Person
                        people = RegPerson.objects.filter(
                            pk=int(result.person_id))
                        result.persons = people

                        # Get OrgUnit
                        porgs_ = None
                        orgunits = RegPersonsOrgUnits.objects.filter(
                            person=int(result.person_id))
                        for orgunit in orgunits:
                            porgs_ = get_vorg_list(orgunit.org_unit_id)
                        result.orgunit = porgs_

                        # Get PlacementID
                        placements = OVCPlacement.objects.filter(
                            placement_id=result.form_id)
                        result.placement = placements
                # print 'resultsets ----------------------%s'%resultsets

            if form_type == 'FTPC':
                for resultset in resultsets:
                    for result in resultset:
                         # Get Person
                        people = RegPerson.objects.filter(
                            pk=int(result.person_id))
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
            form = OVC_FT3hForm(data=request.POST)
            now = timezone.now()
            form_id = request.POST.get('case_id')
            person = request.POST.get('person')

            # OVC_Reporting
            is_self_reporter = request.POST.get('is_self_reporter')
            if(is_self_reporter):
                case_reporter_first_name = 'SELF-REPORTER'
                case_reporter_other_names = 'SELF-REPORTER'
                case_reporter_surname = 'SELF-REPORTER'
                case_reporter_relationship_to_child = 'NONE'
            else:
                case_reporter_first_name = request.POST.get(
                    'case_reporter_first_name')
                case_reporter_other_names = request.POST.get(
                    'case_reporter_other_names')
                case_reporter_surname = request.POST.get(
                    'case_reporter_surname')
                case_reporter_relationship_to_child = request.POST.get(
                    'case_reporter_relationship_to_child')
            case_reporter_contacts = request.POST.get('case_reporter_contacts')
            date_case_opened = request.POST.get('date_case_opened')
            if date_case_opened:
                date_case_opened = convert_date(date_case_opened)

            # OVCCaseGeo
            report_subcounty = request.POST.get('report_subcounty')
            report_ward = request.POST.get('report_ward')
            report_village = request.POST.get('report_village')
            occurence_subcounty = request.POST.get('occurence_subcounty')
            occurence_ward = request.POST.get('occurence_ward')
            occurence_village = request.POST.get('occurence_village')

            # OVC_Details
            person = request.POST.get('person')
            household_economic_status = request.POST.get('household_economics')
            family_status = request.POST.get('family_status')
            hobbies = request.POST.get('hobbies')
            friends = request.POST.get('friends')

            # OVC_Medical_SubConditions
            mental_subconditions = request.POST.getlist('mental_subcondition')
            physical_subconditions = request.POST.getlist(
                'physical_subcondition')
            other_subconditions = request.POST.getlist('other_subcondition')

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
            refferal_to = request.POST.getlist('refferal_to')
            refferal_reason = request.POST.get('refferal_reason')
            refferal_destination_type = request.POST.get(
                'refferal_destination_type')
            refferal_destination_description = request.POST.get(
                'refferal_destination_description')

            # OVCCaseRecord
            ovccr = OVCCaseRecord.objects.get(case_id=id)
            ovccr.case_serial = serial_number
            ovccr.place_of_event = place_of_event
            ovccr.perpetrator_first_name = perpetrator_first_name.upper()
            ovccr.perpetrator_other_names = perpetrator_other_names.upper()
            ovccr.perpetrator_surname = perpetrator_surname.upper()
            ovccr.perpetrator_relationship_type = perpetrator_relationship
            ovccr.case_nature = case_nature
            ovccr.risk_level = risk_level
            ovccr.date_case_opened = date_case_opened
            ovccr.case_reporter_first_name = case_reporter_first_name
            ovccr.case_reporter_surname = case_reporter_surname
            ovccr.case_reporter_contacts = case_reporter_contacts
            ovccr.case_reporter_relationship_to_child = case_reporter_relationship_to_child
            ovccr.case_status = 'ACTIVE'
            ovccr.case_remarks = case_remarks
            ovccr.refferal_reason = refferal_reason
            ovccr.refferal_destination_type = refferal_destination_type
            ovccr.refferal_destination_description = refferal_destination_description
            ovccr.timestamp_updated = now
            ovccr.save(update_fields=['place_of_event',
                                      'case_serial',
                                      'perpetrator_first_name',
                                      'perpetrator_other_names',
                                      'perpetrator_surname',
                                      'perpetrator_relationship_type',
                                      'case_nature',
                                      'risk_level',
                                      'date_case_opened',
                                      'case_reporter_first_name',
                                      'case_reporter_surname',
                                      'case_reporter_contacts',
                                      'case_reporter_relationship_to_child',
                                      'case_status',
                                      'case_remarks',
                                      'refferal_reason',
                                      'refferal_destination_type',
                                      'refferal_destination_description',
                                      'timestamp_updated'])

            # OVCCaseGeo
            ovcgeo = OVCCaseGeo.objects.get(case_id=id)
            ovcgeo.report_subcounty = SetupGeography.objects.get(
                pk=int(report_subcounty))
            ovcgeo.report_ward = report_ward
            ovcgeo.report_village = report_village
            ovcgeo.occurence_subcounty = SetupGeography.objects.get(
                pk=int(occurence_subcounty))
            ovcgeo.occurence_ward = occurence_ward
            ovcgeo.occurence_village = occurence_village
            ovcgeo.timestamp_updated = now
            ovcgeo.save(update_fields=['report_subcounty',
                                       'report_ward',
                                       'report_village',
                                       'occurence_subcounty',
                                       'occurence_ward',
                                       'occurence_village'])

            # OVCDetails
            ovcd = OVCDetails.objects.get(case_id=id)
            ovcd.family_status_id = family_status
            ovcd.household_economic_status = household_economic_status
            ovcd.timestamp_updated = now
            ovcd.save(update_fields=['family_status_id',
                                     'household_economic_status',
                                     'timestamp_updated'])

            # OVCHobbies
            hobbies_exist = OVCHobbies.objects.filter(case_id=id)
            if hobbies_exist:
                OVCHobbies.objects.filter(case_id=id).delete()
            if hobbies:
                hobbies = str(hobbies).split(",")
                for hobby in hobbies:
                    OVCHobbies(
                        case_id=OVCCaseRecord.objects.get(pk=id),
                        hobby=hobby.upper(),
                        timestamp_created=now,
                        person=RegPerson.objects.get(pk=int(person))).save()
            # OVCFriends
            ovcfrnds_exist = OVCFriends.objects.filter(case_id=id)
            if ovcfrnds_exist:
                OVCFriends.objects.filter(case_id=id).delete()
            if friends:
                friends = str(friends).split(",")
                for i, friend in enumerate(friends):
                    names = (friends[i]).split()
                    if(len(names) == 1):
                        ffname = names[0]
                        foname = 'XXXX'
                        fsname = 'XXXX'
                    if(len(names) == 2):
                        ffname = names[0]
                        foname = names[1]
                        fsname = 'XXXX'
                    elif(len(names) == 3):
                        ffname = names[0]
                        foname = names[1]
                        fsname = names[2]
                    OVCFriends(
                        case_id=OVCCaseRecord.objects.get(case_id=id),
                        friend_firstname=ffname.upper(),
                        friend_other_names=foname.upper(),
                        friend_surname=fsname.upper(),
                        timestamp_created=now,
                        person=RegPerson.objects.get(pk=int(person))).save()
            # OVCMedical
            ovcmed = OVCMedical.objects.get(case_id=id)
            ovcmed.mental_condition = mental_condition
            ovcmed.physical_condition = physical_condition
            ovcmed.other_condition = other_condition
            ovcmed.timestamp_updated = now
            ovcmed.save(update_fields=['mental_condition',
                                       'physical_condition',
                                       'other_condition',
                                       'timestamp_updated'])

            # OVCMedicalSubconditions
            """ Delete SubConditions if Captured Erroniously """
            med_conditions = []
            medical_id_ = None
            if ovcmed:
                medical_id_ = ovcmed.medical_id

            if not mental_condition == "MNRM":
                print 'We are here'
                OVCMedicalSubconditions.objects.filter(
                    medical_id=medical_id_, medical_condition='Mental').delete()

                for i, mental_subcondition in enumerate(mental_subconditions):
                    mental_subcondition = mental_subcondition.split(',')
                    for mcondition in mental_subcondition:
                        OVCMedicalSubconditions(
                            medicalsubcond_id=new_guid_32(),
                            medical_id=OVCMedical.objects.get(pk=medical_id_),
                            medical_condition='Mental',
                            medical_subcondition=mcondition,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()
            if not physical_condition == "PNRM":
                OVCMedicalSubconditions.objects.filter(
                    medical_id=medical_id_, medical_condition='Physical').delete()
                for i, physical_subcondition in enumerate(physical_subconditions):
                    physical_subcondition = physical_subcondition.split(',')
                    for pcondition in physical_subcondition:
                        OVCMedicalSubconditions(
                            medicalsubcond_id=new_guid_32(),
                            medical_id=OVCMedical.objects.get(pk=medical_id_),
                            medical_condition='Physical',
                            medical_subcondition=pcondition,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()
            if not other_condition == "CHNM":
                OVCMedicalSubconditions.objects.filter(
                    medical_id=medical_id_, medical_condition='Other').delete()
                for i, other_subcondition in enumerate(other_subconditions):
                    other_subcondition = other_subcondition.split(',')
                    for ocondition in other_subcondition:
                        OVCMedicalSubconditions(
                            medicalsubcond_id=new_guid_32(),
                            medical_id=OVCMedical.objects.get(pk=medical_id_),
                            medical_condition='Other',
                            medical_subcondition=ocondition,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))).save()
            """
            # OVCCaseCategory
            global jsonObjectArray
            old_case_grouping_ids = []
            if jsonObjectArray:
                for jsonObject in jsonObjectArray:
                    new_case_grouping_id = new_guid_32()
                    old_case_grouping_id = jsonObject['case_grouping_id']
                    old_case_grouping_ids.append(old_case_grouping_id)
                    case_category = jsonObject['case_category']
                    date_of_event = jsonObject['date_of_event']
                    if date_of_event:
                        date_of_event = convert_date(str(date_of_event))

                    # Replace Categorys - Maintain case_grouping_id
                    for i, category in enumerate(case_category):
                        OVCCaseCategory(
                            case_category_id=new_guid_32(),
                            case_id=OVCCaseRecord.objects.get(pk=id),
                            case_category=category,
                            case_grouping_id=new_case_grouping_id,
                            date_of_event=date_of_event,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))
                        ).save()

               # Remove Case Categorys Where case_grouping_id = case_grouping_id 
                OVCCaseCategory.objects.filter(
                    case_grouping_id=old_case_grouping_ids[0]).delete()
                jsonObjectArray = []
            """

            # OVCReferral
            existing_refferals = []
            ovcrefs = OVCReferral.objects.filter(case_id=id)
            for ovcref in ovcrefs:
                existing_refferals.append(str(ovcref.refferal_to))
            """ Cater for Unchecked yet Pre-existed """
            for i, erefferal_to in enumerate(existing_refferals):
                if not(str(erefferal_to) in refferal_to):
                    OVCReferral.objects.filter(
                        case_id=id, refferal_to=erefferal_to).delete()
            """ Cater for new selected refferals """
            for i, refferall_to in enumerate(refferal_to):
                if not (str(refferall_to) in existing_refferals):
                    OVCReferral(
                        case_id=OVCCaseRecord.objects.get(pk=id),
                        refferal_to=refferall_to,
                        timestamp_updated=now,
                        person=RegPerson.objects.get(pk=int(person))).save()

            # OVCNeeds
            ovc_imm_needs_exist = OVCNeeds.objects.filter(
                case_id=id, need_type='IMMEDIATE')
            if ovc_imm_needs_exist:
                OVCNeeds.objects.filter(
                    case_id=id, need_type='IMMEDIATE').delete()
            immediate_needs = str(immediate_needs).split(",")
            for immediate_need in immediate_needs:
                OVCNeeds(
                    case_id=OVCCaseRecord.objects.get(pk=id),
                    need_description=immediate_need.upper(),
                    need_type='IMMEDIATE',
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))
                ).save()
            ovc_fut_needs_exist = OVCNeeds.objects.filter(
                case_id=id, need_type='FUTURE')
            if ovc_fut_needs_exist:
                OVCNeeds.objects.filter(
                    case_id=id, need_type='FUTURE').delete()
            future_needs = str(future_needs).split(",")
            for future_need in future_needs:
                OVCNeeds(
                    case_id=OVCCaseRecord.objects.get(pk=id),
                    need_description=future_need.upper(),
                    need_type='FUTURE',
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))
                ).save()

            # FormsAuditTrail
            f = FormsAuditTrail.objects.get(form_id=id)
            f.timestamp_updated = now
            f.save(update_fields=['timestamp_updated'])
        else:
            # Get PersonId/Init Data
            f = FormsAuditTrail.objects.get(form_id=id)
            person_id = int(f.person_id)
            init_data = RegPerson.objects.filter(pk=person_id)
            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)

            # Get OVCDetails
            results_details = OVCDetails.objects.get(case_id=id)

            # Get OVCMedical
            results_med = OVCMedical.objects.get(case_id=id)

            # Get OVCMedicalSubconditions
            _physical_subconditions = []
            _mental_subconditions = []
            _other_subconditions = []
            medical_id = results_med.medical_id
            results_medsubs = OVCMedicalSubconditions.objects.filter(
                medical_id=medical_id)
            if results_medsubs:
                for results_medsub in results_medsubs:
                    if results_medsub.medical_condition == 'Physical':
                        _physical_subconditions.append(
                            results_medsub.medical_subcondition)
                    if results_medsub.medical_condition == 'Mental':
                        _mental_subconditions.append(
                            results_medsub.medical_subcondition)
                    if results_medsub.medical_condition == 'Other':
                        _other_subconditions.append(
                            results_medsub.medical_subcondition)

            # Get OVCCaseRecord
            results_case = OVCCaseRecord.objects.get(case_id=id)
            reporter = results_case.case_reporter_first_name
            is_self_reporter = None
            if 'SELF' in reporter:
                is_self_reporter = 'on'

            # Get OVCCaseGeo
            results_geo = OVCCaseGeo.objects.get(case_id=id)

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

            # Get OVCNeeds
            results_imm_needs = OVCNeeds.objects.filter(
                case_id=id, need_type='IMMEDIATE')
            results_imm = []
            for results_imm_need in results_imm_needs:
                results_imm_ = str(results_imm_need.need_description)
                results_imm.append(results_imm_)

            results_fut_needs = OVCNeeds.objects.filter(
                case_id=id, need_type='FUTURE')
            results_fut = []
            for results_fut_need in results_fut_needs:
                results_fut_ = str(results_fut_need.need_description)
                results_fut.append(results_fut_)

            # Get OVCReferral
            referrals = []
            results_ref = OVCReferral.objects.filter(case_id=id)
            for result_ref in results_ref:
                referrals.append(result_ref.refferal_to)

            # Get OVCCaseCategory
            case_grouping_ids = []
            jsonCategorysData = []
            resultsets = []
            ovcccats = OVCCaseCategory.objects.filter(case_id=id)
            """ Get case_grouping_ids[] """
            for ovcccat in ovcccats:
                case_grouping_id = str(ovcccat.case_grouping_id)
                if not case_grouping_id in case_grouping_ids:
                    case_grouping_ids.append(str(case_grouping_id))
            """ Get Case Categories """
            ovcccats2 = None
            for case_grouping_id in case_grouping_ids:
                ovcccats2 = OVCCaseCategory.objects.filter(
                    case_grouping_id=case_grouping_id)
                for ovcccat in ovcccats2:
                    jsonCategorysData.append({'case_category': ovcccat.case_category,
                                              'date_of_event': ovcccat.date_of_event,
                                              'case_grouping_id': str(ovcccat.case_grouping_id)
                                              })
            """ Create resultsets """
            resultsets.append(jsonCategorysData)

            # Initiaize OVC_FT3hForm()
            form = OVC_FT3hForm({
                'person': person_id,

                # Tab 1
                'is_self_reporter': is_self_reporter,
                'case_reporter_first_name': results_case.case_reporter_first_name,
                'case_reporter_other_names': results_case.case_reporter_other_names,
                'case_reporter_surname': results_case.case_reporter_surname,
                'case_reporter_contacts': results_case.case_reporter_contacts,
                'case_reporter_relationship_to_child': results_case.case_reporter_relationship_to_child,
                'date_case_opened': (results_case.date_case_opened).strftime('%d-%b-%Y'),
                'report_subcounty': results_geo.report_subcounty.area_id,
                'report_ward': results_geo.report_ward,
                'report_village': results_geo.report_village,
                'occurence_subcounty': results_geo.occurence_subcounty.area_id,
                'occurence_ward': results_geo.occurence_ward,
                'occurence_village': results_geo.occurence_village,
                # Tab 2
                'household_economics': results_details.household_economic_status,
                'family_status': results_details.family_status_id,
                'friends': results_frnd,
                'hobbies': results_hob,
                # Tab 3
                'mental_condition': results_med.mental_condition,
                'mental_subcondition': _mental_subconditions,
                'physical_condition': results_med.physical_condition,
                'physical_subcondition': _physical_subconditions,
                'other_condition': results_med.other_condition,
                'other_subcondition': _other_subconditions,
                # Tab 4
                'serial_number': results_case.case_serial,
                'perpetrator_first_name': results_case.perpetrator_first_name,
                'perpetrator_other_names': results_case.perpetrator_other_names,
                'perpetrator_surname': results_case.perpetrator_surname,
                'perpetrator_relationship': results_case.perpetrator_relationship_type,
                'place_of_event': results_case.place_of_event,
                'case_nature': results_case.case_nature,
                'risk_level': results_case.risk_level,
                'immediate_needs': results_imm,
                'future_needs': results_fut,
                'case_remarks': results_case.case_remarks,
                'refferal_to': referrals,
                'refferal_reason': results_case.refferal_reason,
                'refferal_destination_type': results_case.refferal_destination_type,
                'refferal_destination_description': results_case.refferal_destination_description

            })

            return render(request, 'forms/edit_case_record_sheet.html',
                          {
                              'form': form,
                              'init_data': init_data,
                              'vals': vals,
                              'resultsets': resultsets
                          })
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
                        'household_economics',
                        'mental_condition_id',
                        'mental_subcondition_id',
                        'physical_condition_id',
                        'physical_subcondition_id',
                        'other_condition_id',
                        'other_subcondition_id',
                        'case_nature_id',
                        'relationship_type_id',
                        'event_place_id',
                        'risk_level_id',
                        'referral_destination_id',
                        # 'intervention_id',
                        'case_category_id',
                        'core_item_id',
                        'case_reporter_relationship_to_child']
        vals = get_dict(field_name=check_fields)

        ovcd = OVCDetails.objects.get(case_id=id)
        ovccr = OVCCaseRecord.objects.get(case_id=id)
        ovcgeo = OVCCaseGeo.objects.get(case_id=id)
        ovcfrnds = OVCFriends.objects.filter(case_id=id)
        ovchobs = OVCHobbies.objects.filter(case_id=id)
        ovcmed = OVCMedical.objects.get(case_id=id)
        ovcccats = OVCCaseCategory.objects.filter(case_id=id)
        ovcneeds = OVCNeeds.objects.filter(case_id=id)
        ovcrefs = OVCReferral.objects.filter(case_id=id)

        # Retrieve Medical Subconditions
        medical_id = ovcmed.medical_id
        ovcphymeds = OVCMedicalSubconditions.objects.filter(
            medical_id=medical_id, medical_condition='Physical')
        ovcmentmeds = OVCMedicalSubconditions.objects.filter(
            medical_id=medical_id, medical_condition='Mental')
        ovcothermeds = OVCMedicalSubconditions.objects.filter(
            medical_id=medical_id, medical_condition='Other')

        # Retrieve CaseCategories
        jsonData = []
        resultsets = []
        case_grouping_ids = []
        """ Get case_grouping_ids[] """
        for ovcccat in ovcccats:
            case_grouping_id = str(ovcccat.case_grouping_id)
            if not case_grouping_id in case_grouping_ids:
                case_grouping_ids.append(str(case_grouping_id))
        """ Get Case Categories """
        ovcccats2 = None
        for case_grouping_id in case_grouping_ids:
            ovcccats2 = OVCCaseCategory.objects.filter(
                case_grouping_id=case_grouping_id)
            for ovcccat in ovcccats2:
                jsonData.append({'case_category': ovcccat.case_category,
                                 'date_of_event': ovcccat.date_of_event,
                                 'case_grouping_id': str(ovcccat.case_grouping_id)
                                 })
        resultsets.append(jsonData)

        return render(request,
                      'forms/view_case_record_sheet.html',
                      {'init_data': init_data,
                       'vals': vals,
                       'ovcd': ovcd,
                       'ovccr': ovccr,
                       'ovcgeo': ovcgeo,
                       'ovcfrnds': ovcfrnds,
                       'ovchobs': ovchobs,
                       'ovcmed': ovcmed,
                       'ovcphymeds': ovcphymeds,
                       'ovcmentmeds': ovcmentmeds,
                       'ovcothermeds': ovcothermeds,
                       'ovcneeds': ovcneeds,
                       'ovcrefs': ovcrefs,
                       'resultsets': resultsets
                       })
    except Exception, e:
        msg = 'An error occured trying to View OVCCaseRecord - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(forms_registry))


def delete_case_record_sheet(request, id):
    now = timezone.now()
    try:
        # OVCCaseRecord
        ovccr = OVCCaseRecord.objects.get(case_id=id)
        ovccr.is_void = True
        ovccr.timestamp_updated = now
        ovccr.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCCaseGeo
        ovcgeo = OVCCaseGeo.objects.get(case_id=id)
        ovcgeo.is_void = True
        ovcgeo.timestamp_updated = now
        ovcgeo.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCDetails
        ovcd = OVCDetails.objects.get(case_id=id)
        ovcd.is_void = True
        ovcd.timestamp_updated = now
        ovcd.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCHobbies
        ovchobs = OVCHobbies.objects.filter(case_id=id)
        for ovchob in ovchobs:
            ovchob.is_void = True
            ovchob.timestamp_updated = now
            ovchob.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCFriends
        ovcfrnds = OVCFriends.objects.filter(case_id=id)
        for ovcfrnd in ovcfrnds:
            ovcfrnd.is_void = True
            ovcfrnd.timestamp_updated = now
            ovcfrnd.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCMedical
        ovcmed = OVCMedical.objects.get(case_id=id)
        ovcmed.is_void = True
        ovcmed.timestamp_updated = now
        ovcmed.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCMedicalSubconditions
        ovcmedsubconds = OVCMedicalSubconditions.objects.filter(
            medical_id=ovcmed.medical_id)
        for ovcmedsubcond in ovcmedsubconds:
            ovcmedsubcond.is_void = True
            ovcmedsubcond.timestamp_updated = now
            ovcmedsubcond.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCCaseCategory
        ovcccats = OVCCaseCategory.objects.filter(case_id=id)
        for ovccat in ovcccats:
            ovccat.is_void = True
            ovccat.timestamp_updated = now
            ovccat.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCReferral
        ovcrs = OVCReferral.objects.filter(case_id=id)
        for ovcr in ovcrs:
            ovcr.is_void = True
            ovcr.timestamp_updated = now
            ovcr.save(update_fields=['is_void', 'timestamp_updated'])

        # OVCNeeds
        ovcneeds = OVCNeeds.objects.filter(case_id=id)
        for ovcneed in ovcneeds:
            ovcneed.is_void = True
            ovcneed.timestamp_updated = now
            ovcneed.save(update_fields=['is_void', 'timestamp_updated'])

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
    form_id = request.POST.get('case_id')
    now = timezone.now()
    msg = ''
    try:
        if request.method == 'POST':

            form = OVC_FT3hForm(data=request.POST)

            # OVC_Reporting
            is_self_reporter = request.POST.get('is_self_reporter')
            if(is_self_reporter):
                case_reporter_first_name = 'SELF-REPORTER'
                case_reporter_other_names = 'SELF-REPORTER'
                case_reporter_surname = 'SELF-REPORTER'
                case_reporter_relationship_to_child = 'NONE'
            else:
                case_reporter_first_name = request.POST.get(
                    'case_reporter_first_name')
                case_reporter_other_names = request.POST.get(
                    'case_reporter_other_names')
                case_reporter_surname = request.POST.get(
                    'case_reporter_surname')
                case_reporter_relationship_to_child = request.POST.get(
                    'case_reporter_relationship_to_child')
            case_reporter_contacts = request.POST.get('case_reporter_contacts')
            date_case_opened = request.POST.get('date_case_opened')
            if date_case_opened:
                date_case_opened = convert_date(date_case_opened)

            # OVCCaseGeo
            report_subcounty = request.POST.get('report_subcounty')
            report_ward = request.POST.get('report_ward')
            report_village = request.POST.get('report_village')
            occurence_subcounty = request.POST.get('occurence_subcounty')
            occurence_ward = request.POST.get('occurence_ward')
            occurence_village = request.POST.get('occurence_village')

            # OVC_Details
            person = request.POST.get('person')
            household_economic_status = request.POST.get('household_economics')
            family_status = request.POST.get('family_status')
            hobbies = request.POST.get('hobbies')
            friends = request.POST.get('friends')

            # OVC_Medical_SubConditions
            mental_subconditions = request.POST.getlist('mental_subcondition')
            physical_subconditions = request.POST.getlist(
                'physical_subcondition')
            other_subconditions = request.POST.getlist('other_subcondition')

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
            refferal_to = request.POST.getlist('refferal_to')
            refferal_reason = request.POST.get('refferal_reason')
            refferal_destination_type = request.POST.get(
                'refferal_destination_type')
            refferal_destination_description = request.POST.get(
                'refferal_destination_description')

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
                    refferal_reason=refferal_reason,
                    refferal_destination_type=refferal_destination_type,
                    refferal_destination_description=refferal_destination_description,
                    case_remarks=case_remarks,
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving case record info : %s' % str(
                        e)
                messages.add_message(request, messages.INFO, msg)

            # OVCCaseCategory
            try:
                for jsonObject in jsonObjectArray:
                    case_grouping_id = new_guid_32(),
                    case_category = jsonObject['case_category']
                    date_of_event = jsonObject['date_of_event']
                    if date_of_event:
                        date_of_event = convert_date(date_of_event)

                    for i, category in enumerate(case_category):
                        OVCCaseCategory(
                            case_category_id=new_guid_32(),
                            case_id=OVCCaseRecord.objects.get(pk=form_id),
                            case_category=category,
                            case_grouping_id=case_grouping_id,
                            date_of_event=date_of_event,
                            timestamp_created=now,
                            person=RegPerson.objects.get(pk=int(person))
                        ).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving case category info : %s' % str(
                        e)
                messages.add_message(request, messages.INFO, msg)

            # OVCCaseGeo
            try:
                OVCCaseGeo(
                    case_id=OVCCaseRecord.objects.get(pk=form_id),
                    report_subcounty=SetupGeography.objects.get(
                        pk=int(report_subcounty)),
                    report_ward=report_ward,
                    report_village=report_village,
                    occurence_subcounty=SetupGeography.objects.get(
                        pk=int(occurence_subcounty)),
                    occurence_ward=occurence_ward,
                    occurence_village=occurence_village,
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving case geo info : %s' % str(
                        e)
                messages.add_message(request, messages.INFO, msg)

            # OVCReferral
            for i, referral in enumerate(refferal_to):
                referral = referral.split(',')
                for ref in referral:
                    OVCReferral(
                        refferal_id=new_guid_32(),
                        refferal_to=ref,
                        # refferal_status = refferal_status,
                        # date_of_referral_event = date_of_referral_event,
                        case_id=OVCCaseRecord.objects.get(pk=form_id),
                        timestamp_created=now,
                        person=RegPerson.objects.get(pk=int(person))).save()

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
            medical_id = new_guid_32()
            try:
                OVCMedical(
                    medical_id=medical_id,
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

            # OVCMedicalSubconditions
            med_conditions = []
            if not mental_condition == "MNRM":
                for i, mental_subcondition in enumerate(mental_subconditions):
                    mental_subcondition = mental_subcondition.split(',')
                    for mcondition in mental_subcondition:
                        med_conditions.append(
                            {"medical_condition": "Mental",
                             "medical_subcondition": mcondition})
            if not physical_condition == "PNRM":
                for i, physical_subcondition in enumerate(physical_subconditions):
                    physical_subcondition = physical_subcondition.split(',')
                    for pcondition in physical_subcondition:
                        med_conditions.append(
                            {"medical_condition": "Physical",
                             "medical_subcondition": pcondition})
            if not other_condition == "CHNM":
                for i, other_subcondition in enumerate(other_subconditions):
                    other_subcondition = other_subcondition.split(',')
                    for ocondition in other_subcondition:
                        med_conditions.append(
                            {"medical_condition": "Other",
                             "medical_subcondition": ocondition})

            for med_condition in med_conditions:
                try:
                    OVCMedicalSubconditions(
                        medicalsubcond_id=new_guid_32(),
                        medical_id=OVCMedical.objects.get(pk=medical_id),
                        medical_condition=med_condition['medical_condition'],
                        medical_subcondition=med_condition[
                            'medical_subcondition'],
                        timestamp_created=now,
                        person=RegPerson.objects.get(pk=int(person))).save()
                except Exception, e:
                    msg = msg + \
                        '\nError occured when saving medical info : %s' % str(
                            e)
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
                    form_type_id='FTPC',
                    timestamp_created=now,
                    person=RegPerson.objects.get(pk=int(person))).save()
            except Exception, e:
                msg = msg + \
                    '\nError occured when saving FormsAuditTrail : %s' % str(e)
                messages.add_message(request, messages.INFO, msg)

        else:
            # Get Subcounty of app_user
            username = request.user.get_username()
            app_user = AppUser.objects.get(username=username)
            user_id = app_user.id

            # Generate UUIDs()
            case_id = new_guid_32()  # uuid_1
            case_category_id = new_guid_32()  # uuid_2

            init_data = RegPerson.objects.filter(pk=id)
            check_fields = ['sex_id']
            vals = get_dict(field_name=check_fields)
            form = OVC_FT3hForm({
                'case_id': case_id,
                'case_category_id': case_category_id,
                'user_id': user_id})
            return render(request, 'forms/case_record_sheet.html', {'form': form,
                                                                    'init_data': init_data,
                                                                    'vals': vals})

    except Exception, e:
        msg = msg + 'Form  save error: (%s)' % (str(e))
        messages.add_message(request, messages.INFO, msg)

        # Delete Related on Exception e
        if OVCCaseCategory.objects.filter(case_id=form_id):
            OVCCaseCategory.objects.filter(case_id=form_id).delete()
        if OVCCaseGeo.objects.filter(case_id=form_id):
            OVCCaseGeo.objects.filter(case_id=form_id).delete()
        if OVCReferral.objects.filter(case_id=form_id):
            OVCReferral.objects.filter(case_id=form_id).delete()
        if OVCDetails.objects.filter(case_id=form_id):
            OVCDetails.objects.filter(case_id=form_id).delete()
        if OVCHobbies.objects.filter(case_id=form_id):
            OVCHobbies.objects.filter(case_id=form_id).delete()
        if OVCFriends.objects.filter(case_id=form_id):
            OVCFriends.objects.filter(case_id=form_id).delete()

        ovcmedicals = OVCMedical.objects.filter(case_id=form_id)
        if ovcmedicals:
            for ovcmedical in ovcmedicals:
                OVCMedicalSubconditions.filter(
                    medical_id=ovcmedical.medical_id).delete()
        if OVCMedical.objects.filter(case_id=form_id):
            OVCMedical.objects.filter(case_id=form_id).delete()
        if OVCNeeds.objects.filter(case_id=form_id):
            OVCNeeds.objects.filter(case_id=form_id).delete()
        if FormsAuditTrail.objects.filter(form_id=form_id):
            FormsAuditTrail.objects.filter(form_id=form_id).delete()
        if OVCCaseRecord.objects.filter(case_id=form_id):
            OVCCaseRecord.objects.filter(case_id=form_id).delete()

        msg = 'Case Record Sheet Save Error.'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(ovc_search))

    msg = 'Case Record Sheet Save Succesfull.'
    messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(ovc_search))


def residential_placement(request):
    check_fields = ['sex_id']
    vals = get_dict(field_name=check_fields)
    if request.method == 'POST':
        form = ResidentialSearchForm(data=request.POST)

        resultsets = None
        resultset = None
        result = None

        person_type = request.POST.get('person_type')
        search_string = request.POST.get('search_name')
        search_criteria = request.POST.get('search_criteria')

        resultsets = get_persons_list(user=request.user, tokens=search_string, wfc_type='TBVC',
                                      search_location=False, search_wfc_by_org_unit=False)

        for resultset in resultsets:
            for result in resultset:
                ovcplcmnts = OVCPlacement.objects.filter(person=result.id)
                result.placement = ovcplcmnts

        return render(request,
                      'forms/residential_placement.html',
                      {'form': form, 'resultsets': resultsets, 'vals': vals})
    else:
        form = ResidentialSearchForm()
        return render(request, 'forms/residential_placement.html', {'form': form, 'vals': vals})


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

    # OVCCaseEventServices
    for c_event in c_events:
        c_eventsvcs = OVCCaseEventServices.objects.filter(
            case_event_id=c_event.case_event_id, is_void=False).order_by('-timestamp_created')

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
    ovcrefs = OVCReferral.objects.filter(case_id=id, is_void=False)

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

    form = OVC_CaseEventForm(
        initial={'case_id': id, })
    return render(request, 'forms/case_events.html',
                  {
                      'form': form, 'vals': vals,
                      'resultsets': resultsets
                  })


def save_encounter(request):
    now = timezone.now()
    case_event_id = new_guid_32()
    user_id = 0

    try:
        if request.method == 'POST':

            # Get app_user
            username = request.user.get_username()
            app_user = AppUser.objects.get(username=username)
            user_id = app_user.id

            case_id = request.POST.get('case_id')
            encounter_notes = request.POST.get('encounter_notes')
            case_category_id = request.POST.get('case_category_id')
            date_of_encounter_event = now

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
            if jsonObjectArrayServices:
                for jsonObject in jsonObjectArrayServices:
                    service_grouping_id = new_guid_32(),
                    service_provided = jsonObject['service_provided']
                    service_provider = jsonObject['service_provider']
                    place_of_service = jsonObject['place_of_service']
                    date_of_encounter_event = jsonObject[
                        'date_of_encounter_event']
                    if date_of_encounter_event:
                        date_of_encounter_event = convert_date(
                            date_of_encounter_event)

                    for i, service in enumerate(service_provided):
                        OVCCaseEventServices(
                            service_provided=str(service),
                            service_provider=str(service_provider),
                            place_of_service=place_of_service,
                            date_of_encounter_event=date_of_encounter_event,
                            service_grouping_id=service_grouping_id,
                            case_event_id=OVCCaseEvents.objects.get(
                                pk=case_event_id),
                            case_category=OVCCaseCategory.objects.get(pk=case_category_id)).save()
        else:
            print 'Not POST'
    except Exception, e:
        print 'Encounter Save Error: %s' % str(e)
    return HttpResponse('Encounter Saved')


def view_encounter(request):
    resultsets = []
    ovc_events = None
    ovc_services = []
    ovc_category_ids = []
    jsonCeData = []
    jsonSvcsData = []
    service_grouping_ids = []

    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')
            ovc_events_svcs = OVCCaseEventServices.objects.filter(
                case_event_id=case_event_id, is_void=False)

            """ Get service_grouping_ids[] """
            for ovc_events_svc in ovc_events_svcs:
                ovc_category_ids.append(
                    str(ovc_events_svc.case_category_id))
                service_grouping_id = str(ovc_events_svc.service_grouping_id)
                if not service_grouping_id in service_grouping_ids:
                    service_grouping_ids.append(str(service_grouping_id))

            """ Get Services Provided """
            # print 'ovc_category_ids ------- %s' %ovc_category_ids
            ovc_events_svcs2 = None
            for service_grouping_id in service_grouping_ids:
                ovc_events_svcs2 = OVCCaseEventServices.objects.filter(
                    service_grouping_id=service_grouping_id)
                for ovc_events_svc2 in ovc_events_svcs2:
                    jsonSvcsData.append({
                        'service_provided': translate(ovc_events_svc2.service_provided),
                        'service_provider': translate(ovc_events_svc2.service_provider),
                        'place_of_service': ovc_events_svc2.place_of_service,
                        'date_of_encounter_event': ovc_events_svc2.date_of_encounter_event,
                        'service_grouping_id': str(ovc_events_svc2.service_grouping_id)
                    })

            """ Create resultsets """
            resultsets.append(jsonSvcsData)

            ovc_events = OVCCaseEvents.objects.filter(
                case_event_id=case_event_id, is_void=False)
            for ovc_event in ovc_events:
                jsonCeData.append({'case_event_type_id': str(ovc_event.case_event_type_id),
                                   'date_of_event': str(ovc_event.date_of_event),
                                   'case_event_notes': str(ovc_event.case_event_notes),                                   
                                   'case_category': ovc_category_ids[0],
                                   'resultsets': resultsets
                                   })
        else:
            print 'Not POST'
    except Exception, e:
        print 'Encounter View Error: %s' % str(e)
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
            case_category_id = request.POST.get('case_category_id')
            # services_provided = request.POST.getlist('services_provided')
            # refferals_completed = request.POST.getlist('refferals_completed')

            # Update OVCCaseEvents
            ovc_ce = OVCCaseEvents.objects.get(pk=case_event_id)
            # ovc_ce.date_of_event = date_of_encounter_event
            ovc_ce.case_event_notes = encounter_notes
            ovc_ce.timestamp_updated = now
            ovc_ce.save(
                update_fields=['date_of_event', 'case_event_notes', 'timestamp_updated'])

            # Update Case Category Id Provided
            ovc_services = OVCCaseEventServices.objects.filter(
                case_event_id=case_event_id)
            for ovc_service in ovc_services:
                ovc_service.case_category = case_category_id
                ovc_service.save(
                    update_fields=['case_category'])
            """
            Cater for Unchecked yet Pre-existed
            if existing_services_provided:
                for i, eservice in enumerate(existing_services_provided):
                    if not(str(eservice) in services_provided):
                        OVCCaseEventServices.objects.filter(
                            case_event_id=case_event_id, service_provided=eservice).delete()

            Cater for new selected service_provided
            if services_provided:
                for i, service_provided in enumerate(services_provided):
                    if not (str(service_provided) in existing_services_provided):
                        service_provided = service_provided.split(',')
                        for service in service_provided:
                            OVCCaseEventServices(
                                service_provided=service,
                                case_category_id=case_category_id,
                                case_event_id=OVCCaseEvents.objects.get(pk=case_event_id)).save()
            """
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
            case_event_id = new_guid_32()

            case_id = request.POST.get('case_id')
            case_category = request.POST.get('case_category_id')
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

            # OVCCaseEventCourt
            for i, court_order in enumerate(court_orders):
                court_order = court_order.split(',')
                for order in court_order:
                    OVCCaseEventCourt(
                        court_order=order,
                        case_event_id=OVCCaseEvents.objects.get(
                            pk=case_event_id),
                        case_category=OVCCaseCategory.objects.get(pk=case_category)).save()
        else:
            print 'Not POST'
    except Exception, e:
        print 'Court Session Save Error: %s' % str(e)
    return HttpResponse('Court Session Saved')


def view_court(request):
    ovc_court_orders = []
    jsonCourtData = []
    ovc_category_ids = []
    try:
        if request.method == 'POST':
            case_event_id = request.POST.get('event_id')

            ovc_court_events = OVCCaseEventCourt.objects.filter(
                case_event_id=case_event_id, is_void=False)
            for ovc_court_event in ovc_court_events:
                ovc_court_orders.append(str(ovc_court_event.court_order))
                ovc_category_ids.append(
                    str(ovc_court_event.case_category))

            ovc_events = OVCCaseEvents.objects.filter(
                case_event_id=case_event_id, is_void=False)
            for ovc_event in ovc_events:
                jsonCourtData.append({'case_event_type_id': str(ovc_event.case_event_type_id),
                                      'date_of_event': str(ovc_event.date_of_event),
                                      'case_event_notes': str(ovc_event.case_event_notes),
                                      'ovc_court_orders': ovc_court_orders,
                                      'ovc_category_ids': ovc_category_ids[0]
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
            case_category_id = request.POST.get('case_category_id')
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

            # Update Case Category Id Provided
            existing_court_orders = []
            ovc_court_orders = OVCCaseEventCourt.objects.filter(
                case_event_id=case_event_id)
            for ovc_court_order in ovc_court_orders:
                existing_court_orders.append(str(ovc_court_order.court_order))
                ovc_court_order.case_category = case_category_id
                ovc_court_order.save(update_fields=['case_category'])

            """Cater for new selected court orders"""
            for i, court_order in enumerate(court_orders):
                if not (str(court_order) in existing_court_orders):
                    court_order = court_order.split(',')
                    for order in court_order:
                        OVCCaseEventCourt(
                            court_order=order,
                            case_event_id=OVCCaseEvents.objects.get(
                                pk=case_event_id),
                            case_category=case_category_id).save()
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


def placement(request):
    form = ResidentialForm()
    return render(request, 'forms/placement.html', {'form': form})


def placement_followup(request, id):
    form = ResidentialFollowupForm({'person': id})
    return render(request, 'forms/placement_followup.html', {'form': form})


def save_placementfollowup(request):
    now = timezone.now()
    try:
        if request.method == 'POST':
            action = request.POST.get('action')
            person = request.POST.get('person')

            if (action == 'ITP' or action == 'CCF' or action == 'HOM' or action == 'TRA'):
                followup_type = request.POST.get('followup_type')
                followup_details = request.POST.get('followup_details')
                followup_outcome = request.POST.get('followup_outcome')                
                followup_date = request.POST.get('followup_date')
                if followup_date:
                    followup_date = convert_date(followup_date)

                OVCPlacementFollowUp(
                    followup_type=followup_type,
                    followup_date=followup_date,
                    followup_details=followup_details,
                    followup_outcome=followup_outcome,
                    person=RegPerson.objects.get(pk=int(person)),
                    timestamp_created=now).save()
            if (action == 'DIS'):
                discharge_type = request.POST.get('discharge_type')
                discharge_date = request.POST.get('discharge_date')
                discharge_reason = request.POST.get('discharge_reason')
                expected_return_date = request.POST.get('expected_return_date')
                actual_return_date = request.POST.get('actual_return_date')
                discharge_comments = request.POST.get('discharge_comments')
                 # Convert dates
                if discharge_date:
                    discharge_date = convert_date(discharge_date)
                else:
                    discharge_date = None
                if expected_return_date:
                    expected_return_date = convert_date(expected_return_date)
                else:
                    expected_return_date = None
                if actual_return_date:
                    actual_return_date = convert_date(actual_return_date)
                else:
                    actual_return_date = None

                OVCDischargeFollowUp(
                    type_of_discharge=discharge_type,
                    date_of_discharge=discharge_date,
                    reason_of_discharge=discharge_reason,
                    expected_return_date=expected_return_date,
                    actual_return_date=actual_return_date,
                    discharge_comments=discharge_comments,
                    person=RegPerson.objects.get(pk=int(person)),
                    timestamp_created=now).save()
            if (action == 'EDU'):
                admitted_to_school = request.POST.get('admmitted_to_school')
                admission_level = request.POST.get('admmission_class')
                admission_sublevel = request.POST.get('admmission_subclass')
                education_comments = request.POST.get('education_comments')

                OVCEducationFollowUp(
                    admitted_to_school=admitted_to_school,
                    admission_level=admission_level,
                    admission_sublevel=admission_sublevel,
                    education_comments=education_comments,
                    person=RegPerson.objects.get(pk=int(person)),
                    timestamp_created=now).save()
            if (action == 'ADV'):
                adverse_events = request.POST.get('adverse_events')
                adverse_medical_events = request.POST.getlist(
                    'adverse_medical_events')
                ovc_adverse = OVCAdverseEventsFollowUp(
                    adverse_condition_id=new_guid_32(),
                    adverse_condition_description=adverse_events,
                    person=RegPerson.objects.get(pk=int(person)),
                    timestamp_created=now)
                ovc_adverse.save()
                ovc_adverse_pk = ovc_adverse.pk

                if adverse_medical_events:
                    for i, medical_events in enumerate(adverse_medical_events):
                        medical_events = medical_events.split(',')
                        for medical_event in medical_events:
                            OVCAdverseMedicalEventsFollowUp(
                                adverse_medical_condition=medical_event,
                                adverse_condition_id=OVCAdverseEventsFollowUp.objects.get(
                                    pk=ovc_adverse_pk),
                                timestamp_created=now).save()
            if (action == 'COT'):
                case_event_id = new_guid_32()

                # Get app_user
                username = request.user.get_username()
                app_user = AppUser.objects.get(username=username)
                user_id = app_user.id

                case_category_id = request.POST.get('court_session_case')
                date_of_court_event = request.POST.get('date_of_court_event')
                if date_of_court_event:
                    date_of_court_event = convert_date(date_of_court_event)
                court_notes = request.POST.get('court_notes')
                court_orders = request.POST.getlist('court_order')
                workforce_member_court = request.POST.getlist(
                    'workforce_member_court')
                case_id = None
                casecategory = OVCCaseCategory.objects.get(pk=case_category_id)
                if casecategory:
                    case_id = OVCCaseRecord.objects.get(
                        pk=casecategory.case_id_id)

                OVCCaseEvents(
                    case_event_id=case_event_id,
                    case_event_type_id='COURT',
                    date_of_event=date_of_court_event,
                    case_event_details='case_event_details',
                    case_event_notes=court_notes,
                    case_id=case_id,
                    app_user=AppUser.objects.get(pk=user_id)
                ).save()

                for i, court_order in enumerate(court_orders):
                    court_order = court_order.split(',')
                    for order in court_order:
                        OVCCaseEventCourt(
                            court_order=order,
                            case_event_id=OVCCaseEvents.objects.get(
                                pk=case_event_id),
                            case_category=OVCCaseCategory.objects.get(pk=case_category_id)).save()

        else:
            print 'Not POST'
    except Exception, e:
        print 'Residential Placement Followup Save Error: %s' % str(e)
    return HttpResponse('Residential Placement Followup Msg')


def save_placement(request):
    try:
        if request.method == 'POST':
            child_firstname = request.POST.get('child_firstname')
            child_lastname = request.POST.get('child_lastname')
            child_surname = request.POST.get('child_surname')
            child_gender = request.POST.get('child_gender')
            child_dob = request.POST.get('child_dob')
            residential_institution_type = request.POST.get(
                'residential_institution_type')
            residential_institution_name = request.POST.get(
                'residential_institution_name')
            admission_date = request.POST.get('admission_date')
            admission_type = request.POST.get('admission_type')
            admission_reason = request.POST.get('admission_reason')
            holding_period = request.POST.get('holding_period')
            has_court_committal_order = request.POST.get(
                'has_court_committal_order')
            court_order_number = request.POST.get('court_order_number')
            court_order_issue_date = request.POST.get('court_order_issue_date')
            committing_court = request.POST.get('committing_court')
            committing_period = request.POST.get('committing_period')
            ob_number = request.POST.get('ob_number')
            free_for_adoption = request.POST.get('free_for_adoption')
            workforce_member_plcmnt = request.POST.get(
                'workforce_member_plcmnt')
            placement_notes = request.POST.get('placement_notes')
            placement_type = request.POST.get('placement_type')
            person_id = request.POST.get('person_id')
            now = timezone.now()

            # Convert dates
            if child_dob:
                child_dob = convert_date(child_dob)
            else:
                child_dob = None
            if admission_date:
                admission_date = convert_date(admission_date)
            else:
                admission_date = None
            if court_order_issue_date:
                court_order_issue_date = convert_date(court_order_issue_date)
            else:
                court_order_issue_date = None

            reg_person_pk = 0
            # RegPerson -- (Child Basic Details)
            if placement_type == 'Emergency':
                person = RegPerson(
                    designation='',
                    email='',
                    first_name=child_firstname.title(),
                    other_names=child_lastname.title(),
                    surname=child_surname.title(),
                    sex_id=child_gender,
                    date_of_birth=child_dob,
                    date_of_death=None,
                    is_void=False)
                person.save()
                reg_person_pk = int(person.pk)

                # Capture RegPersonTypes Model
                RegPersonsTypes(
                    person_id=reg_person_pk,
                    person_type_id='TBVC',
                    date_began=now,
                    date_ended=None,
                    is_void=False).save()

            if placement_type == 'Normal':
                reg_person_pk = int(person_id)
            # OVCPlacement
            OVCPlacement(
                residential_institution_type=residential_institution_type,
                residential_institution_name=residential_institution_name,
                admission_date=admission_date,
                admission_type=admission_type,
                admission_reason=admission_reason,
                holding_period=holding_period,
                has_court_committal_order=has_court_committal_order,
                court_order_number=court_order_number,
                court_order_issue_date=court_order_issue_date,
                committing_court=committing_court,
                committing_period=committing_period,
                ob_number=ob_number,
                free_for_adoption=free_for_adoption,
                # workforce_member_plcmnt=workforce_member_plcmnt,
                placement_notes=placement_notes,
                placement_type=placement_type,
                person=RegPerson.objects.get(pk=int(reg_person_pk))
            ).save()

        else:
            print 'Not POST'
    except Exception, e:
        msg = 'Residential Placement Save Error: %s' % str(e)
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse(residential_placement))
    msg = 'Residential Placement save succesfull'
    messages.add_message(request, messages.INFO, msg)
    return HttpResponseRedirect(reverse(residential_placement))


def view_placement(request, id):
    form = ResidentialForm()
    return render(request, 'forms/placement_followup.html', {'form': form})


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

            # Update OVCPlacement
            ovc_plcmnt = OVCPlacement.objects.get(
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
            ovc_plcmnts = OVCPlacement.objects.filter(
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


def manage_case_events(request):
    try:
        if request.method == 'POST':
            case_id = request.POST.get('case_id')
            jsonCaseEventsData = []
            case_event_type = None

            # OVCCaseEvents
            c_events = OVCCaseEvents.objects.filter(
                case_id=case_id, is_void=False).order_by('-timestamp_created')

            for c_event in c_events:
                case_event_description = []
                case_event_category = []
                case_event_date = []

                if c_event.case_event_type_id == 'SERVICES':
                    case_event_type = 'SERVICES'
                    servicesData = OVCCaseEventServices.objects.filter(
                        case_event_id=c_event.case_event_id)                   

                    if servicesData:
                        for serviceData in servicesData:
                            case_event_description.append(
                                translate(serviceData.service_provided))
                            case_event_date.append(
                                serviceData.timestamp_created)
                            casecategorys = OVCCaseCategory.objects.filter(
                                    case_category=serviceData.case_category_id, is_void=False)
                            print 'casecategorys --------- %s' %casecategorys
                if c_event.case_event_type_id == 'COURT':
                    case_event_type = 'COURT'
                    courtsData = OVCCaseEventCourt.objects.filter(
                        case_event_id=c_event.case_event_id)
                    if courtsData:
                        for courtData in courtsData:
                            case_event_description.append(
                                translate(courtData.court_order))
                            case_event_date.append(courtData.timestamp_created)
                if c_event.case_event_type_id == 'PLACEMENT':
                    case_event_type = 'PLACEMENT'
                    placementsData = OVCPlacement.objects.filter(
                        case_event_id=c_event.case_event_id)
                    if placementsData:
                        for placementData in placementsData:
                            case_event_description.append(
                                placementData.residential_institution)
                            case_event_date.append(placementData.timestamp_created)

                #the_date = convert_date(case_event_date[0], '%Y-%m-%d')
                case_event_date = case_event_date[0].strftime('%d-%b-%Y')
                jsonCaseEventsData.append({
                    'case_event_type': case_event_type,
                    'case_event_id': c_event.case_event_id,
                    'case_event_category': case_event_category,
                    'case_event_description': case_event_description,
                    'case_event_date': str(case_event_date)
                })
                
    except Exception, e:
        print 'Load Case Events Error: %s' % str(e)
    return JsonResponse(jsonCaseEventsData,
                        content_type='application/json',
                        safe=False)


def manage_refferal(request):
    try:
        if request.method == 'POST':
            now = timezone.now()
            action = request.POST.get('action')
            jsonManageReferralData = []

            case_id = request.POST.get('case_id')
            person_pk = OVCCaseRecord.objects.get(case_id=case_id)
            """ Extract Json Data """
            jsonReferralsObject = request.POST.get('ReferralsData')
            referrals_data = json.loads(jsonReferralsObject)
            case_category = referrals_data['refferal_case']
            refferals_made = referrals_data['refferals_made']

            referral_grouping_id = new_guid_32()
            for i, refferal_made in enumerate(refferals_made):
                refferal_made = refferal_made.split(',')
                for referral in refferal_made:
                    OVCReferral(
                        refferal_id=new_guid_32(),
                        refferal_to=referral,
                        referral_grouping_id=referral_grouping_id,
                        # refferal_status = 'PENDING',
                        # date_of_referral_event = date_of_referral_event,
                        case_category=case_category,
                        timestamp_created=now,
                        case_id=OVCCaseRecord.objects.get(
                            pk=case_id),
                        person=RegPerson.objects.get(pk=int(person_pk.person_id))).save()
            jsonManageReferralData.append(
                {'referral_grouping_id': referral_grouping_id})
    except Exception, e:
        print 'Manage Referral Error: %s' % str(e)
    return JsonResponse(jsonManageReferralData,
                        content_type='application/json',
                        safe=False)


def manage_refferal001(request):
    try:
        if request.method == 'POST':
            # Remove Existing Referral
            referral_grouping_id = request.POST.get('referral_grouping_id')
            OVCReferral.objects.filter(
                referral_grouping_id=referral_grouping_id).delete()
    except Exception, e:

        print 'Manage Referral001 Error: %s' % str(e)
    return HttpResponse('Manage Encounter001 Success : List.Append()')


def manage_refferal002(request):
    try:
        if request.method == 'POST':
            jsonReferralData = []
            case_id = request.POST.get('case_id')

            # Get Referrals to Use to return json
            ovcreferrals = OVCReferral.objects.filter(case_id=case_id)
            for ovcreferral in ovcreferrals:
                jsonReferralData.append({
                    'refferal_id': ovcreferral.refferal_id,
                    'refferal_to': translate(ovcreferral.refferal_to),
                    'refferal_status': ovcreferral.refferal_status,
                    'refferal_enddate': ovcreferral.refferal_enddate,
                    'refferal_case_category': ovcreferral.case_category})
    except Exception, e:
        print 'Manage Referral002 Error: %s' % str(e)
    return JsonResponse(jsonReferralData,
                        content_type='application/json',
                        safe=False)


def manage_refferal003(request):
    try:
        if request.method == 'POST':
            now = timezone.now()
            jsonReferralData = []
            case_category_id = None
            jsonObject = request.POST.get('ReferralsData')
            referrals_data = json.loads(jsonObject)

            if referrals_data:
                refferal_id = referrals_data['refferal_id']
                case_category_ids = referrals_data['case_category_ids']
                refferal_enddate = referrals_data['date_referral_completed']
                if refferal_enddate:
                    refferal_enddate = convert_date(refferal_enddate)

                # Attach CaseCategoryId if Any
                if case_category_ids:
                    if len(case_category_ids) > 1:
                        for case_category_id in case_category_ids:
                            print 'case_category_id -------------------- %s' % case_category_id
                    else:
                        # Just One Case Attached For The Referral
                        case_category_id = case_category_ids[0]

                # Update OVCReferral Model
                ovcref = OVCReferral.objects.get(refferal_id=refferal_id)
                ovcref.refferal_enddate = refferal_enddate
                ovcref.case_category = case_category_id
                ovcref.refferal_status = 'COMPLETED'
                ovcref.timestamp_updated = now
                ovcref.save(
                    update_fields=[
                        'refferal_enddate',
                        'case_category',
                        'timestamp_updated',
                        'refferal_status'
                    ])
    except Exception, e:
        print 'Manage Referral003 Error: %s' % str(e)
    return JsonResponse(jsonReferralData,
                        content_type='application/json',
                        safe=False)


def manage_encounters001(request):
    try:
        if request.method == 'POST':
            jsonObject = request.POST.get('EncountersData')
            data = json.loads(jsonObject)
            jsonObjectArrayServices.append(data)
        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage Encounter001 Error: %s' % str(e)
    return HttpResponse('Manage Encounter001 Success : List.Append()')


def manage_encounters004(request):
    # Pull Case Categories From Db on Edit #
    try:
        service_provided_list = []
        place_of_service_list = []
        date_of_encounter_event_list = []
        jsonServicesData = []

        if request.method == 'POST':
            service_grouping_id = request.POST.get('service_grouping_id')

            ovcservices = OVCCaseEventServices.objects.filter(
                service_grouping_id=service_grouping_id, is_void=False)

            for ovcservice in ovcservices:
                service_provided_list.append(str(ovcservice.service_provided))
                place_of_service_list.append(str(ovcservice.place_of_service))
                date_of_encounter_event_list.append(
                    str(ovcservice.date_of_encounter_event))
            jsonServicesData.append({'service_provided_list': service_provided_list,
                                     'place_of_service_list': place_of_service_list,
                                     'date_of_encounter_event_list': date_of_encounter_event_list
                                     })
        else:
            print 'Not POST'
    except Exception, e:
        print 'Pull Encounters From Db on Edit: %s' % str(e)
    return JsonResponse(jsonServicesData, content_type='application/json',
                        safe=False)


def manage_casecategory001(request):
    try:
        if request.method == 'POST':
            jsonObject = request.POST.get('CaseManagementData')
            data = json.loads(jsonObject)
            jsonObjectArray.append(data)
        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage CaseCategory001 Error: %s' % str(e)
    return HttpResponse('Manage CaseCategory001 Success : List.Append()')


def manage_casecategory002(request):
    try:
        if request.method == 'POST':
            index = int(request.POST.get('index'))
            jsonObjectArray.pop(index - 1)
        else:
            print 'Not POST'
    except Exception, e:
        print 'Manage Referral002 Error: %s' % str(e)
    return HttpResponse('Manage Referral002 Success : List.Remove()')


def manage_casecategory003(request):
    global jsonObjectArray
    jsonObjectArray = []
    return HttpResponse('Manage Referral003 Success : List.Remove(All)')


def manage_casecategory004(request):
    # Pull Case Categories From Db on Edit #
    try:
        case_category_list = []
        date_of_event_list = []
        jsonCaseCategorysData = []

        if request.method == 'POST':
            case_grouping_id = request.POST.get('span_case_grouping_id')

            ovcccats = OVCCaseCategory.objects.filter(
                case_grouping_id=case_grouping_id, is_void=False)

            for ovcccat in ovcccats:
                case_category_list.append(str(ovcccat.case_category))
                date_of_event_list.append(str(ovcccat.date_of_event))

            jsonCaseCategorysData.append({'case_category_list': case_category_list,
                                          'date_of_event_list': date_of_event_list
                                          })

        else:
            print 'Not POST'
    except Exception, e:
        print 'Pull Case Categories From Db on Edit: %s' % str(e)
    return JsonResponse(jsonCaseCategorysData, content_type='application/json',
                        safe=False)


def getJsonObject001(request):
    jsonCaseCategories = []

    try:
        if request.method == 'POST':
            case_id = request.POST.get('case_id')
            action = int(request.POST.get('action'))

            if action == 1:
                # Load for CaseEvents
                ovcccats = OVCCaseCategory.objects.filter(
                    case_id=case_id, is_void=False)
                if ovcccats:
                    for ovcccat in ovcccats:
                        jsonCaseCategories.append({'case_category_id': ovcccat.case_category_id,
                                                   'case_category': translate(ovcccat.case_category)})
            if action == 2:
                # Load for ResidentialPlacementFollowup
                person = request.POST.get('person')
                ovcccats = OVCCaseCategory.objects.filter(
                    person=person, is_void=False)
                if ovcccats:
                    for ovcccat in ovcccats:
                        jsonCaseCategories.append({'case_category_id': ovcccat.case_category_id,
                                                   'case_category': translate(ovcccat.case_category)})
        else:
            print 'getJsonObject001 - Not a POST'
    except Exception, e:
        print '  Error: %s' % str(e)
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
