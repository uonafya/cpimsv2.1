# forms.py
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import AppUser


class RegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('First name'), 'class': 'form-control',
               'autofocus': 'true'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Last name'), 'class': 'form-control',
               'autofocus': 'true'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Username'), 'class': 'form-control',
               'autofocus': 'true'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'), 'class': 'form-control',
               'autofocus': 'true'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': _('Re-enter password'), 'class': 'form-control',
               'autofocus': 'true'}))
    phone_no = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Phone number'), 'class': 'form-control',
               'autofocus': 'true'}))
    national_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('National id number'), 'class': 'form-control',
               'autofocus': 'true'}))
    list_geolocation_id = forms.IntegerField(widget=forms.TextInput(
        attrs={'placeholder': _('Geo-location'), 'class': 'form-control',
               'autofocus': 'true'}))
    staff_no = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': _('Staff number'), 'class': 'form-control',
               'autofocus': 'true'}))

    def clean_username(self):
        try:
            user = AppUser.objects.get(
                username__iexact=self.cleaned_data['username'])
        except AppUser.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(
            "The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


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


class RolesForm(forms.Form):
    user_id = forms.CharField(widget=forms.HiddenInput)
    group_SCM = forms.BooleanField(label=_('System Configuration'))
    group_RGM = forms.BooleanField()
    group_ACM = forms.BooleanField()
    group_SWM = forms.BooleanField()
    group_STD = forms.BooleanField()
    reset_password = forms.BooleanField()

    ACTIVATE_CHOICES = (('activate', 'Activate (May not log into CPIMS)',),
                        ('deactivate', 'Deactivate (May not log into CPIMS)',))
    activate_choice = forms.ChoiceField(
        widget=forms.RadioSelect, choices=ACTIVATE_CHOICES)


class RolesOrgUnits(forms.Form):
    org_unit_id = forms.CharField(widget=forms.HiddenInput)
    org_unit_name = forms.CharField(widget=forms.HiddenInput)
    group_RGU = forms.BooleanField()
    group_DUU = forms.BooleanField()
    group_DSU = forms.BooleanField()
    group_DEC = forms.BooleanField()


class RolesGeoArea(forms.Form):
    sub_county = forms.CharField(widget=forms.HiddenInput)
    area_id = forms.CharField(widget=forms.HiddenInput)
    area_welfare = forms.BooleanField()