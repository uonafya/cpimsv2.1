from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from .functions import get_org_units, get_all_geo_list, get_geo_list
from cpovc_main.functions import get_list, get_org_units_list
from .models import RegPerson


geo_list = get_geo_list(get_all_geo_list(), 'GDIS')
person_type_list = get_list('person_type_id', 'All Types')
org_unit_type_list = get_list('org_unit_type_id', 'All Types')
relationship_type_list = get_list('relationship_type_id', 'All Types')
external_id_list  = get_list('identifier_type_id', 'All Types')
cadre_type_list  = get_list('cadre_type_id', 'All Types')
sex_id_list = get_list('sex_id', 'Select Gender')
psearch_criteria_list = get_list('psearch_criteria_type_id','Select Criteria')
org_units_list = get_org_units_list(True)

class RegistrationSearchForm(forms.Form):
    person_type = forms.ChoiceField(choices=person_type_list,
                                 initial='0',
                                 required=True,
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                     'id':'person_type',
                                     'data-parsley-required': 'true'})
                                 )
   
    search_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Search . . .'), 
               'class': 'form-control',
               'id':'search_name',
               'data-parsley-group': 'primary',
               'data-parsley-required': 'true'}))

    search_criteria = forms.ChoiceField(choices=psearch_criteria_list,
                                 initial='0',
                                 required=True,
                                 widget=forms.Select(
                                     attrs={'class': 'form-control',
                                     'id':'search_criteria',
                                     'data-parsley-required': 'true'})
                                 )
    person_deceased = forms.CharField(required=False,
     widget=forms.CheckboxInput(
        attrs={'class': 'form-control',
         'id':'person_deceased'}))


class RegistrationForm(forms.Form):
    person_type = forms.ChoiceField(choices=person_type_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'person_type',
                                               'data-parsley-required': 'true'}))
    cadre_type = forms.ChoiceField(choices=cadre_type_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'cadre_type',
                                               'data-parsley-required': 'true'}))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First Name'),
               'class': 'form-control',
               'id': 'first_name',
               'data-parsley-required': "true"}))
    other_names = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Other Names'),
               'class': 'form-control',
               'id': 'other_names'}))
    surname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Surname'),
               'class': 'form-control',
               'id': 'surname',
               'data-parsley-required': "true"}))
    sex_id = forms.ChoiceField(choices=sex_id_list,
                               initial='ALL',
                               widget=forms.Select(
                                   attrs={'placeholder': _('Sex'),
                                          'class': 'form-control',
                                          'id': 'sex_id',
                                          'data-parsley-required': "true"})
                               )
    des_phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Phone Number'),
               'class': 'form-control',
               'id': 'des_phone_number',
               'data-parsley-type': 'digits'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Email Address'),
               'class': 'form-control',
               'id': 'email',
               'data-parsley-type': 'email'}))
    living_in = forms.ChoiceField(choices=geo_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'living_in',
                                               #'multiple': 'multiple',
                                               'data-parsley-required': 'true'}))
    org_unit_id = forms.ChoiceField(choices=get_org_units,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'org_unit_id',
                                               'multiple': 'multiple',
                                               'data-parsley-required': 'true'}))
    national_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('National ID'),
               'class': 'form-control',
               'id': 'national_id'}))
    staff_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Staff Number'),
               'class': 'form-control',
               'id': 'staff_id'}))
    workforce_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Workforce ID'),
               'class': 'form-control',
               'id': 'workforce_id'}))
    beneficiary_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Beneficiary ID'),
               'class': 'form-control',
               'id': 'beneficiary_id'}))
    birth_reg_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Birth Reg ID'),
               'class': 'form-control',
               'id': 'birth_reg_id'}))
    caregiver_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Caregiver National ID/Name/CPIMS ID'),
               'class': 'form-control',
               'id': 'caregiver_id'}))
    relationship_type_id = forms.ChoiceField(choices=relationship_type_list,
                                    initial='0',
                                    widget=forms.Select(
                                        attrs={'class': 'form-control',
                                               'id': 'relationship_type_id',
                                               'multiple': 'multiple'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Birth'),
               'class': 'form-control',
               'id': 'date_of_birth',
               'data-parsley-required': 'true'
               }))
    date_of_death = forms.DateField(widget=forms.TextInput(
        attrs={'placeholder': _('Date Of Death'),
               'class': 'form-control',
               'id': 'date_of_death'}))
    class Meta:
        model = RegPerson


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'), 'class': 'form-control input-lg',
               'autofocus': 'true'}),
        error_messages={'required': 'Please enter your username.',
                        'invalid': 'Please enter a valid username.'})
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'), 'class': 'form-control input-lg',
               'autofocus': 'true'}),
        error_messages={'required': 'Please enter your password.',
                        'invalid': 'Please enter a valid password.'},)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise forms.ValidationError("Please enter your username.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Please enter your password.")
        return password


class NewUser(forms.Form):

    # load org_unit_type_list
    org_unit_type_list = get_list('org_unit_type_id', True)

    person_id = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Person ID'),
               'class': 'form-control',
               'id': 'person_id',
               'autofocus': 'true',
               'type': 'hidden',
               'data-parsley-required': "true"}))

    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'),
               'class': 'form-control',
               'id': 'username',
               'autofocus': 'true',
               'data-parsley-required': "true"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password 1'),
               'class': 'form-control',
               'id': 'password1',
               'autofocus': 'true',
               'data-parsley-required': "true"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password 2'),
               'class': 'form-control',
               'id': 'password2',
               'autofocus': 'true'}))


class UserSearchForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Type Name'),
               'class': 'form-control',
               'autofocus': 'true',
               'data-parsley-group': 'primary'}))
    user_void = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control', 'autofocus': 'true'}))


class FormRegistry(forms.Form):
    reg_list = get_list('org_unit_type_id', 'All Types')
    org_type = forms.ChoiceField(
        choices=reg_list,
        initial='0',
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control'}))
    org_unit_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Organisation unit'), 'class': 'form-control',
               'autofocus': 'true', 'data-parsley-required': "true",
               'data-parsley-group': 'primary'}))
    org_closed = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control', 'autofocus': 'true'}))


class FormRegistryNew(forms.Form):
    reg_list = get_list('org_unit_type_id', 'Select unit type')
    reg_type = get_list('identifier_type_id', 'Select registration type')
    all_list = get_all_geo_list()
    county_list = get_geo_list(all_list, 'GPRV')
    sub_county_list = get_geo_list(all_list, 'GDIS')
    ward_list = get_geo_list(all_list, 'GWRD')
    org_unit_type = forms.ChoiceField(
        choices=reg_list,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'true',
                   'data-parsley-required': 'true',
                   'data-parsley-group': 'primary1'}))
    org_reg_type = forms.ChoiceField(
        choices=reg_type,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'true',
                   'data-parsley-isngo': '#id_org_unit_type',
                   'data-parsley-validate-if-empty': 'true'}))
    org_unit_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Unit name'),
                   'class': 'form-control',
                   'autofocus': 'true',
                   'data-parsley-required': "true",
                   'data-parsley-group': 'primary'}))
    reg_date = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Select date'),
                   'class': 'form-control',
                   'autofocus': 'true',
                   'data-parsley-required': "true",
                   'data-parsley-group': 'primary',
                   'id': 'datepicker'}))
    legal_reg_number = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _('Registration No.'),
                   'class': 'form-control',
                   'autofocus': 'true',
                   'data-parsley-isngo': "#id_org_unit_type",
                   'data-parsley-validate-if-empty': "true"}))
    county = forms.MultipleChoiceField(
        choices=county_list,
        label=_('Select County'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'rows': '6',
                   'data-parsley-multiple': 'multiple'}))
    sub_county = forms.MultipleChoiceField(
        choices=sub_county_list,
        label=_('Select sub-county'),
        required=False,
        widget=forms.SelectMultiple(
            attrs={'rows': '6',
                   'data-parsley-chkcounty': '#id_org_unit_type',
                   'data-parsley-validate-if-empty': "true",
                   'data-parsley-multiple': 'multiple'}))
    ward = forms.MultipleChoiceField(
        choices=ward_list, label=_('Select ward'),
        required=False, widget=forms.SelectMultiple(
            attrs={'rows': '6', 'data-parsley-multiple': 'multiple'}))
    parent_org_unit = forms.ChoiceField(
        choices=get_org_units,
        initial='0',
        widget=forms.Select(
            attrs={'class': 'form-control',
                   'autofocus': 'true',
                   'data-parsley-ishq': '#id_org_unit_type',
                   'data-parsley-validate-if-empty': 'true'}))
    close_date = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Select date'),
               'class': 'form-control',
               'autofocus': 'true',
               'data-parsley-withother': "2",
               'id': 'editdate',
               'readonly': 'readonly'}))


class FormContact(forms.Form):
    contacts = get_list('contact_detail_type_id')
    helper = FormHelper()
    helper.form_tag = False
    helper.label_class = 'control-label col-md-4 col-sm-4'
    helper.field_class = 'col-md-6 col-sm-6'
    helper.layout = Layout()

    def __init__(self, *args, **kwargs):
        # extra = kwargs.pop('extra')
        # data-parsley-type="email"
        # data-parsley-type="number"
        txt_box = ['CPOA', 'CPHA']
        attrs = {'class': 'form-control'}
        super(FormContact, self).__init__(*args, **kwargs)
        for i, contact in enumerate(self.contacts):
            contact_key = contact[0]
            contact_name = contact[1]
            v_name, v_check = 'data-parsley-required', "false"
            if 'number' in contact_name.lower():
                v_name, v_check = 'data-parsley-type', "number"
            if 'email' in contact_name.lower():
                v_name, v_check = 'data-parsley-type', "email"
            # validations params
            attrs[v_name] = v_check
            is_designate = 'designated' in contact_name.lower()
            is_postal = 'postal' in contact_name.lower()
            if is_designate or is_postal:
                attrs['data-parsley-required'] = "true"
                del(attrs['data-parsley-type'])
            form_char = forms.CharField(label=contact_name, required=False,
                                        widget=forms.TextInput(
                                            attrs=attrs))
            attrs['rows'] = '3'
            form_text = forms.CharField(label=contact_name, required=False,
                                        widget=forms.Textarea(
                                            attrs=attrs))
            form_type = form_text if str(contact_key) in txt_box else form_char
            self.fields['contact_%s' % contact_key] = form_type

    def extra_contacts(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('contact'):
                field_name = name.replace('contact_', '')
                # field_label = self.fields[name].label
                yield (field_name, value)
