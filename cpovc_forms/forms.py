from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list

person_type_list = get_list('person_type_id', 'Please Select')
psearch_criteria_list = get_list('psearch_criteria_type_id', 'Select Criteria')
form_type_list = get_list('form_type_id', 'Please Select')
religion_type_list = get_list('religion_type_id', 'Please Select')
yesno_list = get_list('yesno_id', 'Please Select')
household_economics_list = get_list('household_economics_id', 'Please Select')
school_category_list = get_list('school_category_id', 'Please Select')
family_status_list = get_list('family_status_id', 'Please Select')
mental_condition_list = get_list('mental_condition_id', 'Please Select')
physical_condition_list = get_list('physical_condition_id', 'Please Select')
other_condition_list = get_list('other_condition_id', 'Please Select')

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
               'data-parsley-group': 'primary',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                        initial='0',
                                        required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control',
                                                   'id': 'search_criteria',
                                                   'data-parsley-required': 'true'})
                                        )

    form_type = forms.ChoiceField(choices=form_type_list,
                                  initial='0',
                                  required=True,
                                  widget=forms.Select(
                                      attrs={'class': 'form-control',
                                             'id': 'form_type_id',
                                             'data-parsley-required': 'true'})
                                  )


class OVCDetailsForm(forms.Form):
    # About Child Info
    religion = forms.ChoiceField(choices=religion_type_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'religion_type',
                                               'data-parsley-required': 'true'})
                                    )
    tribe = forms.CharField(widget=forms.TextInput(
          attrs={'placeholder': _('Tribe'),
                 'class': 'form-control',
                 'id': 'tribe',
                 'data-parsley-required': 'true'}))
    friends = forms.CharField(widget=forms.TextInput(
          attrs={'placeholder': _('Enter Friends separated with commas'),
                 'class': 'form-control',
                 'id': 'friends'}))
    hobbies = forms.CharField(widget=forms.TextInput(
          attrs={'placeholder': _('Enter Hobbies separated with commas'),
                 'class': 'form-control',
                 'id': 'Hobbies'}))

    #Medical Info
    mental_condition = forms.ChoiceField(choices=mental_condition_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'mental_condition',
                                               'data-parsley-required': 'true'})
                                    )
    physical_condition = forms.ChoiceField(choices=physical_condition_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'physical_condition',
                                               'data-parsley-required': 'true'})
                                    )
    other_condition = forms.ChoiceField(choices=other_condition_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'other_condition',
                                               'data-parsley-required': 'true'})
                                    )



    #School Info
    child_in_school = forms.ChoiceField(choices=yesno_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'child_in_school',
                                               'data-parsley-required': 'true'})
                                    )
    school_name = forms.CharField(widget=forms.TextInput(
          attrs={'placeholder': _('School Name'),
                 'class': 'form-control',
                 'id': 'school_name',
                 'data-parsley-required': 'true'}))
    class_ = forms.CharField(widget=forms.TextInput(
          attrs={'placeholder': _('School Name'),
                 'class': 'form-control',
                 'id': 'class_',
                 'data-parsley-required': 'true',
                 'data-parsley-type':'integer'}))
    school_category = forms.ChoiceField(choices=school_category_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'school_category',
                                               'data-parsley-required': 'true'})
                                    )


    # Household Info
    household_economics = forms.ChoiceField(choices=household_economics_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'household_economics',
                                               'data-parsley-required': 'true'})
                                    )
    family_status = forms.ChoiceField(choices=family_status_list,
                                    initial='0',
                                    required=True,
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'family_status',
                                               'data-parsley-required': 'true'})
                                    )

    # Siblings Info
    have_siblings = forms.CharField(required=False,
                                    widget=forms.CheckboxInput(
                                        attrs={'class': 'form-control',
                                                'id':'have_siblings'}))