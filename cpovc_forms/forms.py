from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list, get_org_units_list
from cpovc_registry.functions import get_geo_list, get_all_geo_list
from cpovc_registry.models import RegOrgUnit
from cpovc_main.models import SchoolList

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
mental_subcondition_list = get_list('mental_subcondition_id', 'Please Select')
physical_condition_list = get_list('physical_condition_id', 'Please Select')
physical_subcondition_list = get_list(
    'physical_subcondition_id', 'Please Select')
other_condition_list = get_list('other_condition_id', 'Please Select')
other_subcondition_list = get_list('other_subcondition_id', 'Please Select')
perpetrator_status_list = get_list('perpetrator_status_id', 'Please Select')
sex_id_list = get_list('sex_id', 'Please Select')
relationship_type_list = get_list('relationship_type_id', 'Please Select')
case_nature_list = get_list('case_nature_id', 'Please Select')
case_category_list = get_list('case_category_id', 'Please Select')
intervention_list = get_list('intervention_id', 'Please Select')
risk_level_list = get_list('risk_level_id', 'Please Select')
event_place_list = get_list('event_place_id', 'Please Select')
referral_destination_list = get_list(
    'referral_destination_id', 'Please Select')
referral_destination_classification_list = get_list('referral_destination_classification', 'Please Select')
geo_list = get_geo_list(get_all_geo_list(), 'GDIS')
referral_to_list = get_list('referral_type_id', 'Please Select')
core_item_list = get_list('core_item_id', '')
court_order_list = get_list('court_order_id', '')
residential_status_list = get_list('residential_status_id', 'Please Select')
document_type_list = get_list('document_tag_id', 'Please Select Document')
all_list = get_all_geo_list()
county_list = [('', 'Please Select')] + list(get_geo_list(all_list, 'GPRV'))
sub_county_list = [('', 'Please Select')] + \
    list(get_geo_list(all_list, 'GDIS'))
ward_list = [('', 'Please Select')] + list(get_geo_list(all_list, 'GWRD'))
institution_type_list = get_list('institution_type_id', 'Please Select')
admission_type_list = get_list('admission_type_id', 'Please Select')
# admission_reason_list = get_list('placement_reason_id', 'Please Select')
admission_reason_list = get_list('admission_reason_id', 'Please Select')
adverse_events_list = get_list('adverse_event_id', 'Please Select')
adverse_medical_list = get_list('new_condition_id', 'Please Select')
discharge_type_list = get_list('discharge_type_id', 'Please Select')
# admission_class_list = get_list('admission_class_id', 'Please Select')
admission_class_list = get_list('class_level_id', 'Please Select')
vocational_training_list = get_list('vocational_training_id', 'Please Select')
service_provider_list = get_list('service_provider_id', 'Please Select')
services_list = get_list('core_item_id', 'Please Select')
court_outcome_list = get_list('court_outcome_id', 'Please Select')
courtsession_type_list = get_list('courtsession_type_id', 'Please Select')
case_reporter_list = get_list('case_reporter_id', 'Please Select')
placementfollowup_type_list = get_list(
    'follow_up_type_id', 'Please Select Followup Type')
alternative_family_care_type_list = get_list(
    'alternative_family_care_type_id', 'Please Select')
type_of_adoption_list = get_list('adoption_id', 'Please Select')
bursary_type_list = get_list('bursary_type_id', 'Select Bursary Type')
school_type_list = get_list('school_category_id', 'Please Select')
term_list = get_list('school_term_id', 'Select Term Awarded')
schoolout_reason_list = get_list('out_of_school_id', 'Please Select')
school_admission_type_list = get_list('school_type_id', 'Please Select')
education_level_list = get_list('class_level_id', 'Please Select')
longterm_needs_list = get_list('long_term_support_id', 'Please Select')
shortterm_needs_list = get_list('immediate_need_id', 'Please Select')
period_list = get_list('period_id', 'Please Select Unit')
parental_status_list = get_list('parental_status_id', 'Please Select')
caseoutcome_list = get_list('closure_outcome_id', 'Please Select')

class OVCSchoolForm(forms.Form):
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group0'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    school_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))


class OVCBursaryForm(forms.Form):
    bursary_type = forms.ChoiceField(choices=bursary_type_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'bursary_type',
                                                'data-parsley-required': "true",
                                                'data-parsley-group': 'group0'
                                                }))
    disbursement_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Disbursement Date'),
               'class': 'form-control',
               'id': 'disbursement_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               # type': 'hidden'
               }))

    amount = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Amount(Ksh)'),
               'class': 'form-control',
               'id': 'amount',
               'data-parsley-required': "true",
               'data-parsley-type': "digits",
               'data-parsley-group': 'group0'
               }))

    year = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Year Awarded(YYYY)'),
               'class': 'form-control',
               'id': 'year',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    term = forms.ChoiceField(choices=term_list,
                             initial='0',
                             widget=forms.Select(
                                 attrs={'class': 'form-control',
                                        'id': 'term',
                                        'data-parsley-required': "true",
                                        'data-parsley-group': 'group0'
                                        }))
    person_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person_id',
               'type': 'hidden'
               }))

    bursary_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'bursary_id',
               'type': 'hidden'}))
    operation_mode = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'operation_mode',
               'type': 'hidden'
               }))


class BackgroundDetailsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BackgroundDetailsForm, self).__init__(*args, **kwargs)        
        # schools_list = [('', 'Please Select')] + list(SchoolList.objects.filter().values_list('school_id', 'school_name'))
        name_of_school = forms.ChoiceField(choices=(),
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'name_of_school',
                                                              'data-parsley-required': "true",
                                                              'data-parsley-group': 'group0'}))
        self.fields['name_of_school'] = name_of_school
    admmitted_to_school = forms.ChoiceField(choices=yesno_list,
                                                initial='0',
                                                widget=forms.Select(
                                                        attrs={'class': 'form-control',
                                                               'id': 'admmitted_to_school',
                                                               'data-parsley-required': "true",
                                                               'data-parsley-group': 'group0'
                                                               }))
    not_in_school_reason = forms.ChoiceField(choices=schoolout_reason_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'not_in_school_reason',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group0'
                                                    }))
    admmission_type = forms.ChoiceField(choices=school_admission_type_list,
                                                initial='0',
                                                widget=forms.Select(
                                                        attrs={'class': 'form-control',
                                                               'id': 'admmission_type',
                                                               'data-parsley-required': "true",
                                                               'data-parsley-group': 'group0'
                                                               }))
    admmission_class = forms.ChoiceField(choices=admission_class_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'admmission_class',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group0'
                                                    }))
    admmission_subclass = forms.ChoiceField(choices=vocational_training_list,
                                            initial='0',
                                            widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'admmission_subclass',
                                                           'data-parsley-required': "true",
                                                           'data-parsley-group': 'group0'
                                                           }))
    admission_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admission_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    education_comments = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Education Comments'),
               'class': 'form-control',
               'id': 'education_comments',
               'data-parsley-group': 'group0',
               'rows': '2'}))
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group0'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    school_ward = forms.ChoiceField(
        choices=(), label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))


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
        attrs={'placeholder': _('Enter Child Name(s)'),
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
        attrs={'placeholder': _('Enter Child Name'),
               'class': 'form-control',
               'id': 'form_person',
               'data-parsley-required': 'true'}))


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
        attrs={'placeholder': _('Enter Child Name(s)'),
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


class ResidentialFollowupForm(forms.Form):
    casecategorys = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'casecategorys',
               'type': 'hidden'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    person = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person',
               'type': 'hidden'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    placement_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'placement_id',
               'type': 'hidden'
               }))
    placementfollowup_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'placementfollowup_id',
               'type': 'hidden'
               }))
    placementfollowup_type = forms.ChoiceField(choices=placementfollowup_type_list,
                                               initial='0',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'placementfollowup_type'
                                                          }))
    placementfollowup_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Followup'),
               'class': 'form-control',
               'id': 'placementfollowup_date'
               }))
    placementfollowup_outcome = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Outcome Of Followup'),
               'class': 'form-control',
               'id': 'placementfollowup_outcome'
               }))
    placementfollowup_details = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Details Of Followup'),
               'class': 'form-control',
               'id': 'placementfollowup_details'
               }))
    adverse_events = forms.ChoiceField(choices=adverse_events_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'adverse_events'
                                                  #'data-parsley-required': "true",
                                                  #'data-parsley-group': 'group0'
                                                  }))
    adverse_event_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Adverse Event'),
               'class': 'form-control',
               'id': 'adverse_event_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    adverse_medical_events = forms.ChoiceField(choices=adverse_medical_list,
                                               initial='0',
                                               widget=forms.SelectMultiple(
                                                   attrs={'class': 'form-control',
                                                          'id': 'adverse_medical_events'
                                                          #'data-parsley-required': "true",
                                                          #'data-parsley-group': 'group0'
                                                          }))
    discharge_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Discharge'),
               'class': 'form-control',
               'id': 'discharge_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    expected_return_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Expected Return Date'),
               'class': 'form-control',
               'id': 'expected_return_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    actual_return_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Actual Return Date'),
               'class': 'form-control',
               'id': 'actual_return_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    discharge_type = forms.ChoiceField(choices=discharge_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                           'id': 'discharge_type'
                                                           #'data-parsley-required': "true",
                                                           #'data-parsley-group': 'group0'
                                                  }))

    def __init__(self, *args, **kwargs):
        super(ResidentialFollowupForm, self).__init__(*args, **kwargs)
        discharge_destination = forms.ChoiceField(choices=org_units_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'discharge_destination'}))
        self.fields['discharge_destination'] = discharge_destination
    discharge_reason = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Discharge Reason'),
               'class': 'form-control',
               'id': 'discharge_reason',
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0',
               'rows': '2'}))
    discharge_comments = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Discharge Comments'),
               'class': 'form-control',
               'id': 'discharge_comments',
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0',
               'rows': '2'}))
    admmitted_to_school = forms.ChoiceField(choices=yesno_list,
                                            initial='0',
                                            widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'admmitted_to_school'
                                                           #'data-parsley-required': "true",
                                                           #'data-parsley-group': 'group0'
                                                           }))
    def __init__(self, *args, **kwargs):
        super(ResidentialFollowupForm, self).__init__(*args, **kwargs)
        # schools_list = [('', 'Please Select')] + list(SchoolList.objects.filter().values_list('school_id', 'school_name'))
        name_of_school = forms.ChoiceField(choices=(),
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'name_of_school'
                                                              # 'data-parsley-required': "true",
                                                              # 'data-parsley-group': 'group0'
                                                              }))
        self.fields['name_of_school'] = name_of_school

    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty'}))
    school_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control'}))

    not_in_school_reason = forms.ChoiceField(choices=schoolout_reason_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'not_in_school_reason'
                                                    # 'data-parsley-required': "true",
                                                    # 'data-parsley-group': 'group0'
                                                    }))
    admmission_type = forms.ChoiceField(choices=school_admission_type_list,
                                                initial='0',
                                                widget=forms.Select(
                                                        attrs={'class': 'form-control',
                                                               'id': 'admmission_type'
                                                               # 'data-parsley-required': "true",
                                                               # 'data-parsley-group': 'group0'
                                                               }))

    admmission_class = forms.ChoiceField(choices=admission_class_list,
                                         initial='0',
                                         widget=forms.SelectMultiple(
                                             attrs={'class': 'form-control',
                                                    'id': 'admmission_class'
                                                    #'data-parsley-required': "true",
                                                    #'data-parsley-group': 'group0'
                                                    }))
    admmission_subclass = forms.ChoiceField(choices=vocational_training_list,
                                            initial='0',
                                            widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'admmission_subclass'
                                                           #'data-parsley-required': "true",
                                                           #'data-parsley-group': 'group0'
                                                           }))
    admmission_to_school_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admmission_to_school_date'
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0'
               }))
    education_comments = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Education Comments'),
               'class': 'form-control',
               'id': 'education_comments',
               #'data-parsley-required': "true",
               #'data-parsley-group': 'group0',
               'rows': '2'}))

    # Court Session
    case_event_id_court = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_court',
               'type': 'hidden'
               }))
    court_outcome = forms.ChoiceField(choices=court_outcome_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'court_outcome'
                                                 }))
    next_hearing_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Hearing Date'),
               'class': 'form-control',
               'id': 'next_hearing_date'
               # type': 'hidden'
               }))
    next_mention_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Mention Date'),
               'class': 'form-control',
               'id': 'next_mention_date'
               # type': 'hidden'
               }))
    court_session_case = forms.ChoiceField(initial='0',
                                           widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'court_session_case'
                                                          }))
    court_session_type = forms.ChoiceField(initial='0',
                                           choices=courtsession_type_list,
                                           widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'court_session_type'
                                                          }))
    date_of_court_event = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Court Session'),
               'class': 'form-control',
               'id': 'date_of_court_event'
               }))
    court_order = forms.ChoiceField(choices=court_order_list,
                                    initial='0',
                                    widget=forms.SelectMultiple(
                                        attrs={'class': 'form-control',
                                               'id': 'court_order'
                                               }))
    court_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'court_notes'}))
    workforce_member_court = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_court'}))


class ResidentialForm(forms.Form):
    # OVCCaseEventPlacement
    def __init__(self, *args, **kwargs):
        super(ResidentialForm, self).__init__(*args, **kwargs)

        org_unit_ids = ['TICC', 'TICA', 'TICH', 'TIRS', 'TIRC', 'TIBI', 'TNRC']
        org_unit_ids0 = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        org_unit_ids.extend(org_unit_ids0)
        org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))

        residential_institution_name = forms.ChoiceField(choices=org_units_list,
          initial='0',
            widget=forms.Select(
            attrs={'class': 'form-control',
            'id': 'residential_institution_name',
            'data-parsley-required': "true",
            'data-parsley-group': 'group1'
            }))
        self.fields['residential_institution_name'] = residential_institution_name

        transfer_from = forms.ChoiceField(choices=org_units_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'transfer_from',
                                                 'data-parsley-required': "true",
                                                 'data-parsley-group': 'group1'
                                                 }))
        self.fields['transfer_from'] = transfer_from


   

    placement_type = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'placement_type',
               'type': 'hidden'
               }))
    person_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'person_id',
               'type': 'hidden'
               }))
    child_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('FirstName'),
               'class': 'form-control',
               'id': 'child_firstname',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    child_lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('LastName'),
               'class': 'form-control',
               'id': 'child_lastname',
               # 'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    child_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'child_surname',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))
    child_gender = forms.ChoiceField(choices=sex_id_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'child_gender',
                                                'data-parsley-required': "true",
                                                'data-parsley-group': 'group0'
                                                }))
    child_dob = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Birth'),
               'class': 'form-control',
               'id': 'child_dob',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    case_category = forms.ChoiceField(initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'case_category',
                                                 # 'data-parsley-required': "true",
                                                 'data-parsley-group': 'group1'
                                                 }))

    residential_institution_type = forms.ChoiceField(choices=institution_type_list,
                                                     initial='0',
                                                     widget=forms.Select(
                                                         attrs={'class': 'form-control',
                                                                'id': 'residential_institution_type',
                                                                'data-parsley-required': "true",
                                                                'data-parsley-group': 'group1'
                                                                }))
    
    admission_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Admission'),
               'class': 'form-control',
               'id': 'admission_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group1'
               # type': 'hidden'
               }))
    admission_type = forms.ChoiceField(choices=admission_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'admission_type',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group1'
                                                  }))
    admission_reason = forms.ChoiceField(choices=admission_reason_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'admission_reason',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': 'group1'
                                                    }))
    holding_period = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Holding Period(days)'),
               'class': 'form-control',
               'id': 'holding_period',
               'data-parsley-required': "true",
               'data-parsley-type': "digits",
               'data-parsley-group': 'group2'
               }))
    """
    current_residential_status = forms.ChoiceField(choices=residential_status_list,
                                                   initial='0',
                                                   widget=forms.Select(
                                                       attrs={'class': 'form-control',
                                                              'id': 'current_residential_status'
                                                              }))
    """
    has_court_committal_order = forms.ChoiceField(choices=yesno_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'has_court_committal_order',
                                                             'data-parsley-required': "true",
                                                             'data-parsley-group': 'group2'
                                                             }))
    court_order_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court Order Number'),
               'class': 'form-control',
               'id': 'court_order_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    court_order_issue_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Court Order'),
               'class': 'form-control',
               'id': 'court_order_issue_date',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               # type': 'hidden'
               }))
    committing_court = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Committing Court'),
               'class': 'form-control',
               'id': 'committing_court',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    committing_period_units = forms.ChoiceField(choices=period_list,
                                                initial='0',
                                                widget=forms.Select(
                                                    attrs={'class': 'form-control',
                                                           'id': 'committing_period_units',
                                                           'data-parsley-required': "true",
                                                           'data-parsley-group': 'group2'
                                                           }))
    committing_period = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Committing Period(Days/Weeks/Months/Years'),
               'class': 'form-control',
               'id': 'committing_period',
               'data-parsley-required': "true",
               'data-parsley-type': "digits",
               'data-parsley-group': 'group2'
               }))
    ob_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('OB Number'),
               'class': 'form-control',
               'id': 'ob_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'
               }))
    free_for_adoption = forms.ChoiceField(choices=yesno_list,
                                          initial='0',
                                          widget=forms.Select(
                                              attrs={'class': 'form-control',
                                                     'id': 'free_for_adoption',
                                                     # 'data-parsley-required': "true",
                                                     'data-parsley-group': 'group2'
                                                     }))
    workforce_member_plcmnt = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce Member/SCCO Name'),
               'class': 'form-control',
               'id': 'workforce_member_plcmnt',
               'data-parsley-required': "true",
               'data-parsley-group': 'group2'}))
    placement_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'placement_notes',
               #'data-parsley-required': "true",
               'data-parsley-group': 'group2'}))
    user_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'user_id',
               'type': 'hidden'
               }))


class ResidentialSearchForm(forms.Form):
    person_type = forms.ChoiceField(choices=person_type_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'person_type',
                                               'data-parsley-required': 'true'})
                                    )

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Enter Child Name(s)'),
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
    # Logged in User
    user_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'user_id',
               'type': 'hidden'
               }))

    # Reporter
    is_self_reporter = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control', 'id': 'is_self_reporter'}))
    date_case_opened = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Case Opening'),
               'class': 'form-control',
               'id': 'date_case_opened',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    case_reporter = forms.ChoiceField(
        choices=case_reporter_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'case_reporter',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"
                   }))
    court_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court Name'),
               'class': 'form-control',
               'id': 'court_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    court_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court/File Number'),
               'class': 'form-control',
               'id': 'court_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    police_station = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Police Station'),
               'class': 'form-control',
               'id': 'police_station',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    ob_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('OB Number'),
               'class': 'form-control',
               'id': 'ob_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'),
               'class': 'form-control',
               'id': 'case_reporter_first_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    case_reporter_other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Middle Names'),
               'class': 'form-control',
               'id': 'case_reporter_other_names',
               'data-parsley-group': "group0"}))
    case_reporter_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
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
    report_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'report_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    report_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'report_ward',
                   'class': 'form-control',
                   #'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    report_village = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Village/Estate'),
               'class': 'form-control',
               'id': 'report_village',
               'data-parsley-group': "group0"}))

    def __init__(self, *args, **kwargs):
        super(OVC_FT3hForm, self).__init__(*args, **kwargs)
        org_units_list___ = get_org_units_list('Please Select Unit')

        report_orgunit = forms.ChoiceField(
          choices=org_units_list___, label=_('Select orgunit'),
          initial='0',
            widget=forms.Select(
            attrs={'id': 'report_orgunit',
             'class': 'form-control',
             'data-parsley-required': "true",
             'data-parsley-group': "group0"}))
        self.fields['report_orgunit'] = report_orgunit
    occurence_county = forms.ChoiceField(
        choices=county_list,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'occurence_county',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    occurence_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'occurence_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    occurence_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'occurence_ward',
                   'class': 'form-control',
                   #'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    occurence_village = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Village/Estate'),
               'class': 'form-control',
               'id': 'occurence_village',
               'data-parsley-group': "group0"}))

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
    row_id = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'row_id',
               'type': 'hidden',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

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
                                      widget=forms.SelectMultiple(
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
    mental_subcondition = forms.ChoiceField(choices=mental_subcondition_list,
                                            initial='0',
                                            required=True,
                                            widget=forms.SelectMultiple(
                                                attrs={'class': 'form-control',
                                                       'id': 'mental_subcondition',
                                                       #'data-parsley-required': "true",
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
    physical_subcondition = forms.ChoiceField(choices=physical_subcondition_list,
                                              initial='0',
                                              required=True,
                                              widget=forms.SelectMultiple(
                                                  attrs={'class': 'form-control',
                                                         'id': 'physical_subcondition',
                                                         #'data-parsley-required': "true",
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
    other_subcondition = forms.ChoiceField(choices=other_subcondition_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.SelectMultiple(
                                               attrs={'class': 'form-control',
                                                      'id': 'other_subcondition',
                                                      #'data-parsley-required': "true",
                                                      'data-parsley-group': 'group2'})
                                           )

    # Case Data - OVCCaseRecord Model
    serial_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Case Serial Number'),
               'class': 'form-control',
               'id': 'serial_number',
               'data-parsley-required': "true",
               'data-parsley-group': 'group3'}))
    perpetrator_status = forms.ChoiceField(choices=perpetrator_status_list,
                                           initial='0',
                                           required=True,
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'perpetrator_status',
                                                      'data-parsley-required': "true",
                                                      'data-parsley-group': 'group3'})
                                           )
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
                                                  'id': 'place_of_event'
                                                  #'data-parsley-required': "true",
                                                  #'data-parsley-group': "group3"
                                                  }))
    case_nature = forms.ChoiceField(choices=case_nature_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'case_nature'
                                               #'data-parsley-required': "true",
                                               #'data-parsley-group': "group3"
                                               }))
    risk_level = forms.ChoiceField(choices=risk_level_list,
                                   initial='0',
                                   widget=forms.Select(
                                       attrs={'class': 'form-control',
                                              'id': 'risk_level',
                                              'data-parsley-required': "true",
                                              'data-parsley-group': "group3"
                                              }))
    immediate_needs = forms.ChoiceField(choices=shortterm_needs_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.SelectMultiple(
                                                attrs={  # 'class': 'form-control',
                                                    'id': 'immediate_needs',
                                                    #'data-parsley-required': "true",
                                                    'data-parsley-group': 'group3'})
                                        )
    future_needs = forms.ChoiceField(choices=longterm_needs_list,
                                     initial='0',
                                     required=True,
                                     widget=forms.SelectMultiple(
                                         attrs={'class': 'form-control',
                                                'id': 'future_needs',
                                                #'data-parsley-required': "true",
                                                'data-parsley-group': 'group3'})
                                     )
    case_remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Case Remarks'),
               'class': 'form-control',
               'id': 'case_remarks',
               'rows': '3',
               'data-parsley-group': "group3"}))

    # Refferals
    refferal_present = forms.ChoiceField(choices=yesno_list,
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'refferal_present',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': "group3"}))
    refferal_destination_type = forms.ChoiceField(choices=referral_destination_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'refferal_destination_type'
                                                             }))
    #refferal_destination_description = forms.CharField(widget=forms.TextInput(
    #    attrs={'placeholder': _('Specify'),
    #           'class': 'form-control',
    #           'id': 'refferal_destination_description'}))
    refferal_destination_description = forms.ChoiceField(choices=referral_destination_classification_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'refferal_destination_description'
                                               }))
    refferal_reason = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Referral Reason'),
               'class': 'form-control',
               'id': 'refferal_reason'}))
    refferal_to = forms.ChoiceField(choices=referral_to_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'refferal_to'
                                               }))
    summon_issued = forms.ChoiceField(choices=yesno_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'summon_issued',
                                                 'data-parsley-required': "true",
                                                 'data-parsley-group': "group3"
                                                 }))
    date_of_summon = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Summon'),
               'class': 'form-control',
               'id': 'date_of_summon',
               'data-parsley-required': "true",
               'data-parsley-group': "group3"
               }))

    date_of_event = forms.DateField(widget=forms.TextInput(
                                    attrs={'placeholder': _('Date'),
                                           'class': 'form-control',
                                           'id': 'date_of_event',
                                           #'data-parsley-required': "true",
                                           'data-parsley-group': "group3"
                                           }))
    case_category = forms.ChoiceField(choices=case_category_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'case_category',
                                                 #'multiple': 'multiple',
                                                 #'data-parsley-required': "true",
                                                 'data-parsley-group': "group3"
                                                 }))
    case_subcategory = forms.MultipleChoiceField(choices=(),
                                                 initial='',
                                                 widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
                                                 'id': 'case_subcategory',
                                                 #'multiple': 'multiple',
                                                 #'data-parsley-required': "true",
                                                 'data-parsley-group': "group3"
                                                 }))
    case_category_list = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'case_category_list',
               'type': 'hidden'
               }))
    referralactors_list = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'referralactors_list',
               'type': 'hidden'
               }))
    clone_ids_list = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'clone_ids_list',
               'type': 'hidden'
               }))
    intervention = forms.ChoiceField(choices=intervention_list,
                                     initial='0',
                                     widget=forms.SelectMultiple(
                                         attrs={'class': 'form-control',
                                                'id': 'intervention',
                                                'multiple': 'multiple',
                                                #'data-parsley-required': "true",
                                                'data-parsley-group': "group3"
                                                }))


class OVC_CaseEventForm(forms.Form):
    service_provided_case = forms.ChoiceField(choices=case_category_list,
                                              initial='0',
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control',
                                                         'id': 'service_provided_case'
                                                         }))
    place_of_service = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Place of Service'),
               'class': 'form-control',
               'id': 'place_of_service'}))
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
    refferal_case = forms.ChoiceField(initial='0',
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control',
                                                         'id': 'refferal_case'
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
    case_event_id_summon = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_summon',
               'type': 'hidden'
               }))
    case_event_id_closure = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_closure',
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
        attrs={'placeholder': _('Date of Service'),
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
    service_provided = forms.ChoiceField(choices=services_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'service_provided'
                                                    }))
    service_provider = forms.ChoiceField(choices=service_provider_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'service_provider'
                                                    }))
    service_provided_list = forms.CharField(widget=forms.TextInput(
        attrs={ 'type': 'hidden',
               'id': 'service_provided_list'}))
    refferals_made = forms.ChoiceField(choices=referral_to_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'refferals_made'
                                                  }))
    refferals_actor = forms.ChoiceField(choices=referral_destination_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'refferals_actor'
                                                   }))
    """
    refferals_actor_specify = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Specify'),
               'class': 'form-control',
               'id': 'refferals_actor_specify'}))
    """
    refferals_actor_specify = forms.ChoiceField(choices=referral_destination_classification_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'refferals_actor_specify'
                                               }))
    refferals_completed = forms.ChoiceField(choices=referral_to_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'refferals_completed'
                                                       }))

    # OVCCaseEventCourt
    court_file_number = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Notes'),
               'class': 'form-control',
               'id': 'court_file_number'}))
    court_outcome = forms.ChoiceField(choices=court_outcome_list,
                                      initial='0',
                                      widget=forms.Select(
                                          attrs={'class': 'form-control',
                                                 'id': 'court_outcome'
                                                 }))
    court_session_type = forms.ChoiceField(initial='0',
                                           choices=courtsession_type_list,
                                           widget=forms.Select(
                                                   attrs={'class': 'form-control',
                                                          'id': 'court_session_type'
                                                          }))
    next_hearing_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Hearing Date'),
               'class': 'form-control',
               'id': 'next_hearing_date'
               # type': 'hidden'
               }))
    next_mention_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Next Mention Date'),
               'class': 'form-control',
               'id': 'next_mention_date'
               # type': 'hidden'
               }))
    court_order = forms.ChoiceField(choices=court_order_list,
                                    initial='0',
                                    widget=forms.SelectMultiple(
                                        attrs={'class': 'form-control',
                                               'id': 'court_order'
                                               }))
    case_event_id_summon = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'case_event_id_summon',
               'type': 'hidden'
               }))
    honoured = forms.ChoiceField(choices=yesno_list,
                                 initial='0',
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                            'id': 'honoured'
                                            }))
    honoured_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Honoured Date'),
               'class': 'form-control',
               'id': 'honoured_date'
               }))
    summon_date = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Next Summon'),
               'class': 'form-control',
               'id': 'summon_date'
               }))
    summon_note = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Summon Notes'),
               'class': 'form-control',
               'rows': '2',
               'id': 'summon_note'}))

    # OVCCaseEventPlacement
    def __init__(self, *args, **kwargs):
        super(OVC_CaseEventForm, self).__init__(*args, **kwargs)
        org_unit_ids = ['TICC', 'TICA', 'TICH', 'TIRS', 'TIRC', 'TIBI']
        org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))
        residential_institution = forms.ChoiceField(choices=org_units_list,
                                                    initial='0',
                                                    widget=forms.Select(
                                                        attrs={'class': 'form-control',
                                                               'id': 'residential_institution'}))
        self.fields['residential_institution'] = residential_institution

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
    case_outcome = forms.ChoiceField(choices=caseoutcome_list,
                                                  initial='0',
                                                  widget=forms.Select(
                                                      attrs={'class': 'form-control',
                                                             'id': 'case_outcome'
                                                             }))
    def __init__(self, *args, **kwargs):
        super(OVC_CaseEventForm, self).__init__(*args, **kwargs)
        # org_unit_ids = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        # org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids).values_list('id', 'org_unit_name'))
        org_units_list = [('', 'Please Select')] + list(RegOrgUnit.objects.all().values_list('id', 'org_unit_name'))
        transfered_to = forms.ChoiceField(choices=org_units_list,
                                                    initial='0',
                                                    widget=forms.Select(
                                                        attrs={'class': 'form-control',
                                                               'id': 'transfered_to'}))
        self.fields['transfered_to'] = transfered_to

    date_of_case_closure = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Closed/Transferred'),
               'class': 'form-control',
               'id': 'date_of_case_closure'
               }))
    case_closure_notes = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Case Closure Notes'),
               'class': 'form-control',
               'id': 'case_closure_notes',
               'rows': '2'
               }))


class OVC_FTFCForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OVC_FTFCForm, self).__init__(*args, **kwargs)
        adopting_agency_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id='TNSA').values_list('id', 'org_unit_name'))
        adopting_agency = forms.ChoiceField(choices=adopting_agency_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'adopting_agency',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': "group0"}))
        self.fields['adopting_agency'] = adopting_agency


        org_unit_ids__ = ['TNGP', 'TNGD']
        children_office_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids__).values_list('id', 'org_unit_name'))
        children_office = forms.ChoiceField(choices=children_office_list,
                                            initial='0',
                                            widget=forms.Select(
                                                attrs={'class': 'form-control',
                                                       'id': 'children_office',
                                                       'data-parsley-required': "true",
                                                       'data-parsley-group': "group0"}))
        self.fields['children_office'] = children_office

        # org_unit_ids___ = ['TICC']
        org_unit_ids___ = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        familycare_institutions_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids___).values_list('id', 'org_unit_name'))
        
        residential_institution_name = forms.ChoiceField(choices=familycare_institutions_list,
                                                         initial='0',
                                                         widget=forms.Select(
                                                             attrs={'class': 'form-control',
                                                                    'id': 'residential_institution_name',
                                                                    'data-parsley-required': "true",
                                                                    'data-parsley-group': 'group0'
                                                                    }))
        self.fields['residential_institution_name'] = residential_institution_name

        # org_unit_ids____ = ['TNSA', 'TNSI', 'TNCI', 'TNRH', 'TNRC', 'TNRR']
        fostered_from_list = [('', 'Please Select')] + list(RegOrgUnit.objects.filter(org_unit_type_id__in=org_unit_ids___).values_list('id', 'org_unit_name'))
        
        fostered_from = forms.ChoiceField(choices=fostered_from_list,
                                                         initial='0',
                                                         widget=forms.Select(
                                                             attrs={'class': 'form-control',
                                                                    'id': 'fostered_from',
                                                                    'data-parsley-required': "true",
                                                                    'data-parsley-group': 'group0'
                                                                    }))
        self.fields['fostered_from'] = fostered_from

    contact_person = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contact Person (Phone)'),
               'class': 'form-control',
               'id': 'contact_person',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))

    type_of_care = forms.ChoiceField(choices=alternative_family_care_type_list,
                                     initial='0',
                                     widget=forms.Select(
                                         attrs={'class': 'form-control',
                                                'id': 'type_of_care',
                                                'data-parsley-required': "true",
                                                'data-parsley-group': "group0"
                                                }))
    
    adoption_subcounty = forms.ChoiceField(choices=sub_county_list,
                                           initial='0',
                                           widget=forms.Select(
                                               attrs={'class': 'form-control',
                                                      'id': 'adoption_subcounty',
                                                      'data-parsley-required': "true",
                                                      'data-parsley-group': "group0"
                                                      }))
    adoption_country = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Specify Country'),
               'class': 'form-control',
               'id': 'adoption_country',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    court_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court Name'),
               'class': 'form-control',
               'id': 'court_name',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    court_file_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Court File Number'),
               'class': 'form-control',
               'id': 'court_file_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"}))
    certificate_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('P&C/Certificate Number'),
               'class': 'form-control',
               'id': 'certificate_number',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    date_of_certificate_expiry = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date of Certificate Expiry'),
               'class': 'form-control',
               'id': 'date_of_certificate_expiry',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    type_of_adoption = forms.ChoiceField(choices=type_of_adoption_list,
                                         initial='0',
                                         widget=forms.Select(
                                             attrs={'class': 'form-control',
                                                    'id': 'type_of_adoption',
                                                    'data-parsley-required': "true",
                                                    'data-parsley-group': "group0"
                                                    }))
    date_of_adoption = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date'),
               'class': 'form-control',
               'id': 'date_of_adoption',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    parental_status = forms.ChoiceField(choices=parental_status_list,
                                        initial='0',
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'parental_status',
                                                   'data-parsley-required': "true",
                                                   'data-parsley-group': "group0"
                                                   }))
    adopting_mother_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('FirstName'),
               'class': 'form-control',
               'id': 'adopting_mother_firstname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_mother_othernames = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Names'),
               'class': 'form-control',
               'id': 'adopting_mother_othernames',
               'data-parsley-group': "group0"
               }))
    adopting_mother_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'adopting_mother_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_mother_idnumber = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('ID/Passport Number'),
               'class': 'form-control',
               'id': 'adopting_mother_idnumber',
               'data-parsley-group': "group0"
               }))
    adopting_mother_contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contacts'),
               'class': 'form-control',
               'id': 'adopting_mother_contacts',
               'data-parsley-group': "group0"
               }))
    adopting_father_firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('FirstName'),
               'class': 'form-control',
               'id': 'adopting_father_firstname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_father_othernames = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Names'),
               'class': 'form-control',
               'id': 'adopting_father_othernames',
               'data-parsley-group': "group0"
               }))
    adopting_father_surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'adopting_father_surname',
               'data-parsley-required': "true",
               'data-parsley-group': "group0"
               }))
    adopting_father_idnumber = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('ID/Passport Number'),
               'class': 'form-control',
               'id': 'adopting_father_idnumber',
               'data-parsley-group': "group0"
               }))
    adopting_father_contacts = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Contacts'),
               'class': 'form-control',
               'id': 'adopting_father_contacts',
               'data-parsley-group': "group0"
               }))
    adoption_remarks = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': _('Remarks'),
               'class': 'form-control',
               'id': 'adoption_remarks',
               'rows': 3,
               'data-parsley-group': "group0"
               }))


## Demo API
class OVCSchoolForm(forms.Form):
    school_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Name of School'),
               'class': 'form-control',
               'id': 'school_name',
               'data-parsley-required': "true",
               'data-parsley-group': 'group0'
               }))

    type_of_school = forms.ChoiceField(choices=school_type_list,
                                       initial='0',
                                       widget=forms.Select(
                                           attrs={'class': 'form-control',
                                                  'id': 'type_of_school',
                                                  'data-parsley-required': "true",
                                                  'data-parsley-group': 'group0'
                                                  }))
    school_subcounty = forms.ChoiceField(
        choices=sub_county_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'school_subcounty',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
    school_ward = forms.ChoiceField(
        choices=ward_list, label=_('Select ward'),
        initial='',
        widget=forms.Select(
            attrs={'id': 'school_ward',
                   'class': 'form-control',
                   'data-parsley-required': "true",
                   'data-parsley-group': "group0"}))
