import json

from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from cpovc_registry.models import RegPerson
from cpovc_main.functions import (convert_date, new_guid_32)

from .models import OVCCareEvents, OVCCareAssessment, OVCCareEAV, OVCCarePriority


def validate_filters(required_filters, data):
    validation = {"validity": True, "field": ""}
    for r_filter in required_filters:
        if not r_filter in data.keys():
            validation = {"validity": False, "field": r_filter}

    return validation


class Form1aView(ListAPIView):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, **kwargs):
        if request.data:
            # check for minimum payload data needed for all scenarios
            minimum_required_filters = [
                'args',
                'person',
            ]

            post_payload_validity = validate_filters(minimum_required_filters,
                                                     request.data['payload'])

            if not post_payload_validity['validity']:
                return JsonResponse(
                    {
                        'status':
                        'bad request',
                        'message':
                        "missing data attribute: " +
                        post_payload_validity['field']
                    },
                    status=400)

            #acutal logoc
            #TODO extract to independent function
            # org_unit = None
            data = request.data.get('payload')
            # ou_primary = data['ou_primary']
            # ou_attached = data['ou_attached']
            # ou_attached = ou_attached.split(',')

            event_type_id = 'FSAM'
            args = int(data['args'])
            person = data['person']

            #Assesments Case 1
            if args == 1:
                #check for required payload data
                assessment_required_filters = [
                    'args', 'person', 'date_of_assessment',
                    'olmis_assessment_provided_list'
                ]

                post_payload_validity = validate_filters(
                    assessment_required_filters, request.data['payload'])

                if not post_payload_validity['validity']:
                    return JsonResponse(
                        {
                            'status':
                            'bad request',
                            'message':
                            "missing data attribute: " +
                            post_payload_validity['field']
                        },
                        status=400)

                date_of_assessment = data['date_of_assessment']
                if date_of_assessment:
                    #TODO import convert_date function
                    date_of_assessment = convert_date(date_of_assessment)

                # Save F1AEvent
                event_counter = OVCCareEvents.objects.filter(
                    event_type_id=event_type_id, person=person,
                    is_void=False).count()
                ovccareevent = OVCCareEvents(
                    event_type_id=event_type_id,
                    event_counter=event_counter,
                    event_score=0,
                    date_of_event=date_of_assessment,
                    created_by=request.user.id,
                    person=RegPerson.objects.get(pk=int(person)))
                ovccareevent.save()
                new_pk = ovccareevent.pk

                # F1A Assessment
                olmis_assessment_provided_list = data[
                    'olmis_assessment_provided_list']
                if olmis_assessment_provided_list:
                    olmis_assessment_data = json.loads(
                        olmis_assessment_provided_list)
                    for assessment_data in olmis_assessment_data:
                        service_grouping_id = new_guid_32()
                        olmis_assessment_domain = assessment_data[
                            'olmis_assessment_domain']
                        olmis_assessment_service = assessment_data[
                            'olmis_assessment_coreservice']
                        olmis_assessment_service_status = assessment_data[
                            'olmis_assessment_coreservice_status']
                        services_status = olmis_assessment_service_status.split(
                            ',')
                        for service_status in services_status:
                            OVCCareAssessment(
                                domain=olmis_assessment_domain,
                                service=olmis_assessment_service,
                                service_status=service_status,
                                event=OVCCareEvents.objects.get(pk=new_pk),
                                service_grouping_id=service_grouping_id).save(
                                )
                return JsonResponse(
                    {
                        'message': "Assessment successfuly saved"
                    }, status=200)

            elif args == 2:
                post_payload_validity = validate_filters(
                    ['date_of_cevent', 'olmis_critical_event'],
                    request.data['payload'])

                if not post_payload_validity['validity']:
                    return JsonResponse(
                        {
                            'status':
                            'bad request',
                            'message':
                            "missing data attribute: " +
                            post_payload_validity['field']
                        },
                        status=400)

                #data payload is valid, hence get the payload information
                data = request.data.get('payload')

                date_of_cevent = data['date_of_cevent']
                if date_of_cevent:
                    date_of_cevent = convert_date(date_of_cevent)

                # Save F1AEvent
                event_counter = OVCCareEvents.objects.filter(
                    event_type_id=event_type_id, person=person,
                    is_void=False).count()
                ovccareevent = OVCCareEvents(
                    event_type_id=event_type_id,
                    event_counter=event_counter,
                    event_score=0,
                    date_of_event=date_of_cevent,
                    created_by=request.user.id,
                    person=RegPerson.objects.get(pk=int(person)))
                ovccareevent.save()
                new_pk = ovccareevent.pk

                # Critical Events [CEVT]
                my_kvals = []
                olmis_critical_event = data['olmis_critical_event']  # DHES
                # for i, cevts in enumerate(olmis_critical_event):
                cevts = olmis_critical_event.split(',')
                for cevt in cevts:
                    my_kvals.append({"entity": "CEVT", "value": cevt})

                for kvals in my_kvals:
                    key = kvals["entity"]
                    value = kvals["value"]
                    attribute = "FSAM"
                    OVCCareEAV(
                        entity=key,
                        attribute=attribute,
                        value=value,
                        event=OVCCareEvents.objects.get(pk=new_pk)).save()
                return JsonResponse(
                    {
                        'message': "Critival event successfuly saved"
                    },
                    status=200)

            elif args == 3:
                minimum_required_filters = [
                    'date_of_priority', 'olmis_priority_service_provided_list'
                ]

                post_payload_validity = validate_filters(
                    minimum_required_filters, request.data['payload'])

                if not post_payload_validity['validity']:
                    return JsonResponse(
                        {
                            'status':
                            'bad request',
                            'message':
                            "missing data attribute: " +
                            post_payload_validity['field']
                        },
                        status=400)

                #data payload is valid, hence get the payload information
                data = request.data.get('payload')

                date_of_priority = data['date_of_priority']
                if date_of_priority:
                    date_of_priority = convert_date(date_of_priority)

                # Save F1AEvent
                event_counter = OVCCareEvents.objects.filter(
                    event_type_id=event_type_id, person=person,
                    is_void=False).count()
                ovccareevent = OVCCareEvents(
                    event_type_id=event_type_id,
                    event_counter=event_counter,
                    event_score=0,
                    date_of_event=date_of_priority,
                    created_by=request.user.id,
                    person=RegPerson.objects.get(pk=int(person)))
                ovccareevent.save()
                new_pk = ovccareevent.pk

                # Priority Needs
                olmis_priority_service_provided_list = data[
                    'olmis_priority_service_provided_list']
                if olmis_priority_service_provided_list:
                    olmis_priority_data = olmis_priority_service_provided_list
                    for priority_data in olmis_priority_data:
                        service_grouping_id = new_guid_32()
                        olmis_priority_domain = priority_data[
                            'olmis_priority_domain']
                        olmis_priority_service = priority_data[
                            'olmis_priority_service']
                        services = olmis_priority_service.split(',')
                        for service in services:
                            OVCCarePriority(
                                domain=olmis_priority_domain,
                                service=service,
                                event=OVCCareEvents.objects.get(pk=new_pk),
                                service_grouping_id=service_grouping_id).save(
                                )
                return JsonResponse(
                    {
                        'message': "Priority Needs successfuly saved"
                    },
                    status=200)

        else:
            return JsonResponse(
                {
                    'error': "Request Payload is empty"
                }, status=400)
