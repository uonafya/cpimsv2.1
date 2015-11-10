from django import forms
from django.utils.translation import ugettext_lazy as _
from cpovc_main.functions import get_list
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from .functions import get_org_units
# from cpovc_main.models import SetupGeography


class FormRegistry(forms.Form):
    reg_list = get_list('org_unit_type_id', 'All Types')
    org_type = forms.ChoiceField(choices=reg_list,
                                 initial='0',
                                 required=False,
                                 widget=forms.Select(
                                     attrs={'class': 'form-control'})
                                 )
    org_unit_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Organisation unit'), 'class': 'form-control',
               'autofocus': 'true', 'data-parsley-required': "true",
               'data-parsley-group': 'primary'}))
    org_closed = forms.CharField(required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control', 'autofocus': 'true'}))


class FormRegistryNew(forms.Form):
    reg_list = get_list('org_unit_type_id', 'Select unit type')
    reg_type = get_list('identifier_type_id', 'Select registration type')

    org_unit_type = forms.ChoiceField(
        choices=reg_list, initial='0', widget=forms.Select(
            attrs={'class': 'form-control', 'autofocus': 'true',
                   'data-parsley-required': 'true'}))
    org_reg_type = forms.ChoiceField(
        choices=reg_type, initial='0', widget=forms.Select(
            attrs={'class': 'form-control', 'autofocus': 'true',
                   'data-parsley-isngo': '#id_org_unit_type',
                   'data-parsley-validate-if-empty': 'true'}))
    org_unit_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Unit name'), 'class': 'form-control',
               'autofocus': 'true', 'data-parsley-required': "true",
               'data-parsley-group': 'primary'}))
    reg_date = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Select date'), 'class': 'form-control',
               'autofocus': 'true', 'data-parsley-required': "true",
               'data-parsley-group': 'primary', 'id': 'datepicker'}))
    sub_county = forms.MultipleChoiceField(
        choices=reg_list, label=_('Select sub-county'),
        required=False, widget=forms.SelectMultiple(
            attrs={'rows': '6'}))
    ward = forms.MultipleChoiceField(
        choices=reg_list, label=_('Select ward'),
        required=False, widget=forms.SelectMultiple(
            attrs={'rows': '6'}))
    parent_org_unit = forms.ChoiceField(
        choices=get_org_units,
        initial='0', widget=forms.Select(
            attrs={'class': 'form-control', 'autofocus': 'true',
                   'data-parsley-ishq': '#id_org_unit_type',
                   'data-parsley-validate-if-empty': 'true'}))


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
        super(FormContact, self).__init__(*args, **kwargs)
        for i, contact in enumerate(self.contacts):
            contact_key = contact[0]
            contact_name = contact[1]
            v_name, v_check = 'data-parsley-required', "false"
            if 'number' in contact_name.lower():
                v_name, v_check = 'data-parsley-type', "number"
            if 'email' in contact_name.lower():
                v_name, v_check = 'data-parsley-type', "email"
            form_char = forms.CharField(label=contact_name, required=False,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   v_name: v_check}))
            form_text = forms.CharField(label=contact_name, required=False,
                                        widget=forms.Textarea(
                                            attrs={'class': 'form-control',
                                                   'rows': 3}))
            form_type = form_text if str(contact_key) in txt_box else form_char
            self.fields['contact_%s' % contact_key] = form_type

    def extra_contacts(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('contact'):
                field_name = name.replace('contact_', '')
                # field_label = self.fields[name].label
                yield (field_name, value)
