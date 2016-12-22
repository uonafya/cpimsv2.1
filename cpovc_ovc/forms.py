"""OVC Registration forms."""
from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list, get_org_units_list

search_criteria_list = (('', 'Select Criteria'), ('1', 'Names'),
                        ('2', 'HouseHold'), ('3', 'CHV'), ('4', 'CBO'))

immunization_list = get_list('immunization_status_id', 'Please Select')

person_type_list = get_list('person_type_id', 'Please Select Type')
school_level_list = get_list('school_level_id', 'Please Select Level')
hiv_status_list = get_list('hiv_status_id', 'Please Select Status')
art_status_list = get_list('art_status_id', 'Please Select Status')
ovc_form_type_list = get_list('ovc_form_type_id', 'Please Select')

health_unit_list = get_org_units_list(
    default_txt='Select Unit', org_types=['HFGU'])


class OVCSearchForm(forms.Form):
    """Search registry form."""

    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search . . .'),
               'class': 'form-control',
               'id': 'search_name',
               'data-parsley-minlength': '3',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(
        choices=search_criteria_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'search_criteria'}))

    person_deceased = forms.CharField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'id': 'person_deceased'}))

    form_type = forms.ChoiceField(
        choices=ovc_form_type_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'id': 'form_type'}))


class OVCRegistrationForm(forms.Form):
    """OVC registration form."""

    def __init__(self, guids, *args, **kwargs):
        """Override methods."""
        super(OVCRegistrationForm, self).__init__(*args, **kwargs)
        for i in guids:
            gid = 'gstatus_%s' % str(i)
            gstatus = forms.ChoiceField(
                choices=hiv_status_list,
                initial='0',
                widget=forms.Select(
                    attrs={'class': 'form-control', 'id': gid,
                           'data-parsley-required': "true"}))
            self.fields[gid] = gstatus

    reg_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'reg_date',
               'data-parsley-required': "true"}))

    has_bcert = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control',
                   'id': 'has_bcert'}))

    bcert_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'bcert_no'}))

    ncpwd_no = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'ncpwd_no'}))

    disb = forms.CharField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-control',
                   'id': 'disb'}))

    cbo_uid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'initial': '00001',
               'id': 'cbo_uid',
               'data-parsley-required': "true"}))

    cbo_uid_check = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control',
               'initial': '00001',
               'id': 'cbo_uid_check'}))

    cbo_id = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control',
               'id': 'cbo_id'}))

    immunization = forms.ChoiceField(
        choices=immunization_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'immunization'}))

    hiv_status = forms.ChoiceField(
        choices=hiv_status_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'hiv_status'}))

    school_level = forms.ChoiceField(
        choices=school_level_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'school_level'}))

    facility = forms.ChoiceField(
        choices=health_unit_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'facility'}))

    art_status = forms.ChoiceField(
        choices=art_status_list,
        initial='0',
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'data-parsley-required': "true",
                   'id': 'art_status'}))

    link_date = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'link_date'}))

    ccc_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control',
               'id': 'ccc_number'}))
