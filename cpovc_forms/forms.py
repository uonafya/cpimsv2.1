from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list
from cpovc_registry.functions import get_geo_list, get_all_geo_list
from cpovc_registry.models import RegOrgUnit

person_type_list = get_list('person_type_id', 'Please Select')
psearch_criteria_list = get_list('psearch_criteria_type_id', 'Select Criteria')
form_type_list = get_list('form_type_id', 'Please Select')
religion_type_list = get_list('religion_type_id', 'Please Select')
yesno_list = get_list('yesno_id', 'Please Select')
household_economics_list = get_list('household_economics', 'Please Select')
school_category_list = get_list('school_category_id', 'Please Select')
class_list = get_list('class_level_id', 'Please Select')
family_status_list = get_list('family_status_id', 'Please Select')
mental_condition_list = get_list('mental_condition_id', 'Please Select')
physical_condition_list = get_list('physical_condition_id', 'Please Select')
other_condition_list = get_list('other_condition_id', 'Please Select')
sex_id_list = get_list('sex_id', 'Please Select')
relationship_type_list = get_list('relationship_type_id', 'Please Select')
case_nature_list = get_list('case_nature_id', 'Please Select')
case_category_list = get_list('case_category_id', 'Please Select')
intervention_list = get_list('intervention_id', 'Please Select')
risk_level_list = get_list('risk_level_id', 'Please Select')
event_place_list = get_list('event_place_id', 'Please Select')
referral_destination_list = get_list(
    'referral_destination_id', 'Please Select')
geo_list = get_geo_list(get_all_geo_list(), 'GDIS')
referral_to_list = get_list('core_item_id', '')
core_item_list = get_list('core_item_id', '')
court_order_list = get_list('court_order_id', '')
residential_status_list = get_list('residential_status_id', 'Please Select')
document_type_list = get_list('document_tag_id', 'Please Select Document')
org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter().values_list(
    'id', 'org_unit_name'))


class DocumentsManager(forms.Form):
    document_type = forms.ChoiceField(choices=document_type_list,
                                      initial='0',
                                      required=True,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'document_type',
                                                 'data-parsley-required': 'true'})
                                      )
    document_description = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Document Description'),
               'class': 'form-control',
               'id': 'document_description',
               'data-parsley-required': 'true'}))
    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search . . .'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-required': 'true'}))
    file_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('File Name'),
               'class': 'form-control',
               'readonly': 'true',
               'id': 'file_name'}))
    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   'data-parsley-required': 'true'})
                                        )
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))


class SearchForm(forms.Form):
    form_type = forms.ChoiceField(choices=form_type_list,
                                  initial='0',
                                  required=True,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'form_type',
                                             'data-parsley-required': 'true'})
                                  )

    form_person = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search Owner. . .'),
               'class': 'form-control',
               'id': 'form_person',
               'data-parsley-group': 'primary_'}))


class OVCSearchForm(forms.Form):
    person_type = forms.ChoiceField(choices=person_type_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'person_type',
                                               'data-parsley-required': 'true'})
                                    )

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search . . .'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-group': 'primary_',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   # 'readonly':'true',
                                                   'data-parsley-required': 'true'})
                                        )

    form_type_search = forms.ChoiceField(choices=form_type_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'form_type_search',
                                                    'data-parsley-required': 'true'})
                                         )


class OVC_FT3hForm(forms.Form):
    # Reporter
    self_reporter = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control',
                   'id': 'self_reporter'}))
    date_case_opened = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Case Opening'),
               'class': 'form-control',
               'id': 'date_case_opened',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    case_reporter_first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Reporter First Name'),
               'class': 'form-control',
               'id': 'case_reporter_first_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Reporter Middle Names'),
               'class': 'form-control',
               'id': 'case_reporter_other_names',
               'data-parsley-group': "group0"}))
    case_reporter_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Reporter Surname'),
               'class': 'form-control',
               'id': 'case_reporter_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Reporter PhoneNumber'),
               'class': 'form-control',
               'id': 'case_reporter_contacts',
               'data-parsley-pattern': '/^[0-9\+]{1,}[0-9\-]{3,15}$/',
               #'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_relationship_to_child = forms.ChoiceField(
        choices=relationship_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'case_reporter_relationship_to_child',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"
                   }))

    # About Child Info
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    case_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'uuid',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    case_category_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'uuid',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    friends = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Friends and press ENTER'),
               'class': 'form-control',
               'id': 'friends',
               'type': 'hidden',
               'data-parsley-group': 'group1'}))
    hobbies = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Hobbies and press ENTER'),
               'class': 'form-control',
               'id': 'hobbies',
               'type': 'hidden',
               'data-parsley-group': 'group1'}))
    case_grouping_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden',
               'data-parsley-group': 'group0'
               }))
    """
    referrals_list = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'referrals_list',
               #'type': 'hidden',
               'data-parsley-group': 'group0'
               }))
    case_category_list = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_category',
               #'type': 'hidden',
               'data-parsley-group': 'group0'
               }))
    intervention_list = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'intervention_list',
               #'type': 'hidden',
               'data-parsley-group': 'group0'
               }))
    """

    # Household Info
    household_economics = forms.ChoiceField(choices=household_economics_list,
                                            initial='0',
                                            required=True,
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'household_economics',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': 'group1'})
                                            )
    family_status = forms.ChoiceField(choices=family_status_list,
                                      initial='0',
                                      required=True,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'family_status',
                                                 'data-parsley-required': "true",
                                                 'data-parsley-group': 'group1'})
                                      )

    # Medical Info
    mental_condition = forms.ChoiceField(choices=mental_condition_list,
                                         initial='0',
                                         required=True,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'mental_condition',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group2'})
                                         )
    physical_condition = forms.ChoiceField(choices=physical_condition_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'physical_condition',
                                                      'data-parsley-required': "true",
                                                      'data-parsley-group': 'group2'})
                                           )
    other_condition = forms.ChoiceField(choices=other_condition_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'other_condition',
                                                   'data-parsley-required': "true",
                                                   'data-parsley-group': 'group2'})
                                        )

    # Case Data - OVCCaseRecord Model
    serial_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Case Serial Number'),
               'class': 'form-control',
               'id': 'serial_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group3'}))
    perpetrator_first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'),
               'class': 'form-control',
               'id': 'perpetrator_first_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group3"}))
    perpetrator_other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Middle Name'),
               'class': 'form-control',
               'id': 'perpetrator_other_names',
               'data-parsley-group': "group3"}))
    perpetrator_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'perpetrator_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group3"}))

    perpetrator_relationship = forms.ChoiceField(choices=relationship_type_list,
                                                 initial='0',
                                                 widget=forms.Select(
                                                     attrs={'class': 'form-control',
                                                            'id': 'perpetrator_relationship',
                                                            'data-parsley-required': "true",
                                                            'data-parsley-group': "group3"
                                                            }))
    place_of_event = forms.ChoiceField(choices=event_place_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'place_of_event',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': "group3"
                                                  }))
    case_nature = forms.ChoiceField(choices=case_nature_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'case_nature',
                                               'data-parsley-required': "true",
                                               'data-parsley-group': "group3"
                                               }))
    risk_level = forms.ChoiceField(choices=risk_level_list,
                                   initial='0',
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'id': 'risk_level',
                                              'data-parsley-required': "true",
                                              'data-parsley-group': "group3"
                                              }))
    immediate_needs = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Needs separated with commas'),
               'class': 'form-control',
               'type': 'hidden',
               'id': 'immediate_needs'}))
    future_needs = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Needs separated with commas'),
               'class': 'form-control',
               'type': 'hidden',
               'id': 'future_needs'}))
    case_remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Case Remarks'),
               'class': 'form-control',
               'id': 'case_remarks',
               'rows': '3',
               'data-parsley-group': "group3"}))

    # Refferals
    refferal_destination_type = forms.ChoiceField(choices=referral_destination_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'refferal_destination_type',
                                                             'data-parsley-required': "true",
                                                             'data-parsley-group': "group3"
                                                             }))
    refferal_reason = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Refferal Reason'),
               'class': 'form-control',
               'id': 'refferal_reason',
               'data-parsley-group': "group3"}))
    refferal_to = forms.ChoiceField(choices=referral_to_list,
                                    initial='0',
                                    widget=forms.SelectMultiple(
                                        attrs={'class': 'form-control',
                                               'id': 'refferal_to',
                                               'multiple': 'multiple',
                                               #'data-parsley-required': "true",
                                               'data-parsley-group': "group4"
                                               }))

    date_of_event = forms.DateField(widget=forms.TextInput(
                                    attrs={'placeholder': _('Date Of Event'),
                                           'class': 'form-control',
                                           'id': 'date_of_event',
                                           #'data-parsley-required': "true",
                                           'data-parsley-group': "group4"
                                           }))
    case_category = forms.ChoiceField(choices=case_category_list,
                                      initial='0',
                                      widget=forms.SelectMultiple(
                                          attrs={'class': 'form-control',
                                                 'id': 'case_category',
                                                 'multiple': 'multiple',
                                                 #'data-parsley-required': "true",
                                                 'data-parsley-group': "group4"
                                                 }))
    intervention = forms.ChoiceField(choices=intervention_list,
                                     initial='0',
                                     widget=forms.SelectMultiple(
                                         attrs={'class': 'form-control',
                                                'id': 'intervention',
                                                'multiple': 'multiple',
                                                #'data-parsley-required': "true",
                                                'data-parsley-group': "group4"
                                                }))


class OVC_CaseEventForm(forms.Form):
    service_provided_case = forms.ChoiceField(choices=case_category_list,
                                              initial='0',
                                              widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                    'id': 'service_provided_case'
                                                    }))
    court_session_case = forms.ChoiceField(initial='0',
                                              widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                    'id': 'court_session_case'
                                                    }))
    placement_case = forms.ChoiceField(initial='0',
                                              widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                    'id': 'placement_case'
                                                    }))
    # Case ID
    case_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_id',
               'type': 'hidden'
               }))
    # Case Event ID
    case_event_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id',
               'type': 'hidden'}))

    case_event_id_svc = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_svc',
               'type': 'hidden'
               }))
    case_event_id_court = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_court',
               'type': 'hidden'
               }))
    case_event_id_plcmt = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_plcmt',
               'type': 'hidden'
               }))

    case_event_type = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_type',
               'type': 'hidden'
               }))
    operation_mode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'operation_mode',
               'type': 'hidden'
               }))

    # OVCCaseEventServices
    workforce_member_svc = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_svc', }))
    workforce_member_court = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_court'}))
    workforce_member_plcmnt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_plcmnt'}))
    date_of_referral_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Completed'),
               'class': 'form-control',
               'name': 'date_of_referral_event',
               'id': 'date_of_referral_event'
               }))
    date_of_court_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Court Session'),
               'class': 'form-control',
               'id': 'date_of_court_event'
               }))
    date_of_encounter_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Encounter/Service'),
               'class': 'form-control',
               'id': 'date_of_encounter_event'
               }))
    date_of_placement_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Placement'),
               'class': 'form-control',
               'id': 'date_of_placement_event'
               }))

    court_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'court_notes'}))
    encounter_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'encounter_notes'}))
    placement_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'placement_notes'}))
    service_provided = forms.ChoiceField(choices=core_item_list,
                                         initial='0',
                                         widget=forms.SelectMultiple(
                                             attrs={'class': 'form-control',
                                                    'id': 'service_provided'
                                                    }))
    refferals_made = forms.ChoiceField(choices=referral_to_list,
                                       initial='0',
                                       widget=forms.SelectMultiple(
                                           attrs={'class': 'form-control',
                                                  'id': 'refferals_made'
                                                  }))
    refferals_completed = forms.ChoiceField(choices=referral_to_list,
                                            initial='0',
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'form-control',
                                                       'id': 'refferals_completed'
                                                       }))

    # OVCCaseEventCourt
    court_file_number = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'court_file_number'}))
    court_order = forms.ChoiceField(choices=court_order_list,
                                    initial='0',
                                    widget=forms.SelectMultiple(
                                        attrs={'class': 'form-control',
                                               'id': 'court_order'
                                               }))

    # OVCCaseEventPlacement
    residential_institution = forms.ChoiceField(choices=org_units_list,
                                                initial='0',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'residential_institution'
                                                           }))
    current_residential_status = forms.ChoiceField(choices=residential_status_list,
                                                   initial='0',
                                                   widget=forms.Select(
                                                       attrs={'class': 'form-control',
                                                              'id': 'current_residential_status'
                                                              }))
    has_court_committal_order = forms.ChoiceField(choices=yesno_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'has_court_committal_order'
                                                             }))
    free_for_adoption = forms.ChoiceField(choices=yesno_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'free_for_adoption'
                                                     }))
    admission_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admission_date'
               }))
    departure_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Departure'),
               'class': 'form-control',
               'id': 'departure_date'
               # type': 'hidden'
               }))

    # OVCCaseEventClosure
    case_status = forms.ChoiceField(choices=yesno_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'case_status'
                                               }))
    case_outcome_notes = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Case Outcome Notes'),
               'class': 'form-control',
               'id': 'case_outcome_notes'
               }))
    date_of_case_closure = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Case Closed'),
               'class': 'form-control',
               'id': 'date_of_case_closure'
               }))
