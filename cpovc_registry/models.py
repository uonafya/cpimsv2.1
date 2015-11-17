from datetime import datetime
from django.db import models
from cpovc_auth.models import AppUser


class RegOrgUnit(models.Model):
    org_unit_id_vis = models.CharField(max_length=12)
    org_unit_name = models.CharField(max_length=255)
    org_unit_type_id = models.CharField(max_length=4)
    date_operational = models.DateField(null=True)
    date_closed = models.DateField(null=True)
    is_void = models.BooleanField(default=False)
    parent_org_unit_id = models.IntegerField(null=True, blank=True)

    def _is_active(self):
        if self.date_closed:
            return False
        else:
            return True

    is_active = property(_is_active)

    class Meta:
        db_table = 'reg_org_unit'

    def make_void(self, date_closed=None):
        self.is_void = True
        if date_closed:
            self.date_closed = date_closed
        super(RegOrgUnit, self).save()


class RegOrgUnitContact(models.Model):
    org_unit = models.ForeignKey(RegOrgUnit)
    contact_detail_type_id = models.CharField(max_length=20)
    contact_detail = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'reg_org_units_contact'


class RegOrgUnitExternalID(models.Model):
    org_unit = models.ForeignKey(RegOrgUnit)
    identifier_type_id = models.CharField(max_length=4)
    identifier_value = models.CharField(max_length=255, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'reg_org_units_external_ids'


class RegOrgUnitGeography(models.Model):
    org_unit = models.ForeignKey(RegOrgUnit)
    area_id = models.IntegerField()
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'reg_org_units_geo'

    def make_void(self, date_delinked=None):
        self.is_void = True
        if date_delinked:
            self.date_delinked = date_delinked
        elif not self.date_delinked:
            self.date_delinked = datetime.now().date()
        super(RegOrgUnitGeography, self).save()


class RegPerson(models.Model):
    #beneficiary_id = models.CharField(max_length=10, null=True, blank=True, default=None)
    #workforce_id = models.CharField(max_length=8, null=True, blank=True, default=None)
    #birth_reg_id = models.CharField(max_length=15, null=True, blank=True, default=None)
    #national_id = models.CharField(max_length=15, null=True, blank=True, default=None)
    #staff_id = models.CharField(max_length=15, null=True, blank=True, default=None)
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, null=True, blank=True, default=None)
    surname = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default=None)
    des_phone_number = models.IntegerField(null=True, default=None)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True, default=None)
    sex_id = models.CharField(max_length=4)
    is_void = models.BooleanField(default=False)

    def _get_persons_data(self):
        _reg_persons_data = RegPerson.objects.all().order_by('-id')
        return _reg_persons_data

    def _get_full_name(self):
        return '%s %s %s' % (self.first_name, self.other_names, self.surname)

    def make_void(self):
        self.is_void = True
        super(RegPerson, self).save()

    def record_death(self, date_of_death=None):
        if date_of_death:
            self.date_of_death = date_of_death
        super(RegPerson, self).save()

    full_name = property(_get_full_name)

    class Meta:
        db_table = 'reg_person'


class RegPersonsGuardians(models.Model):
    child_person = models.ForeignKey(RegPerson)
    guardian_person_id = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    def make_void(self, date_delinked=None):
        self.is_void = True
        if date_delinked:
            self.date_delinked = date_delinked
        super(RegPersonsGuardians, self).save()

    class Meta:
        db_table = 'reg_persons_guardians'


class RegPersonsTypes(models.Model):
    person = models.ForeignKey(RegPerson)
    person_type_id = models.CharField(max_length=4)
    date_began = models.DateField(null=True)
    date_ended = models.DateField(null=True, default=None)
    is_void = models.BooleanField(default=False)

    def make_void(self, person_type_change_date=None):
        self.is_void = True
        if person_type_change_date:
            self.date_ended = person_type_change_date
        super(RegPersonsTypes, self).save()

    class Meta:
        db_table = 'reg_persons_types'


class RegPersonsGeo(models.Model):
    person = models.ForeignKey(RegPerson)
    area_id = models.IntegerField()
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    def make_void(self, date_delinked, is_void):
        if date_delinked:
            self.date_delinked = date_delinked
        self.is_void = True
        super(RegPersonsGeo, self).save()

    class Meta:
        db_table = 'reg_persons_geo'


class RegPersonsExternalIds(models.Model):
    person = models.ForeignKey(RegPerson)
    identifier_type_id = models.CharField(max_length=4)
    identifier = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)

    def make_void(self):
        self.is_void = True
        super(RegPersonsExternalIds, self).save()

    class Meta:
        db_table = 'reg_persons_external_ids'


class RegPersonsContact(models.Model):
    person = models.ForeignKey(RegPerson)
    contact_detail_type_id = models.CharField(max_length=4)
    contact_detail = models.CharField(max_length=255)
    is_void = models.BooleanField(default=False)

    def make_void(self):
        self.is_void = True
        super(RegPersonsContact, self).save()

    class Meta:
        db_table = 'reg_persons_contact'


class RegPersonsOrgUnits(models.Model):
    person = models.ForeignKey(RegPerson)
    org_unit_id = models.ForeignKey(RegOrgUnit)
    date_linked = models.DateField(null=True)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'reg_persons_org_units'


class RegPersonsWorkforceIds(models.Model):
    person = models.ForeignKey(RegPerson)
    workforce_id = models.CharField(max_length=8, null=True)

    class Meta:
        db_table = 'reg_persons_workforce_ids'


class RegPersonsBeneficiaryIds(models.Model):
    person = models.ForeignKey(RegPerson)
    beneficiary_id = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'reg_persons_beneficiary_ids'


class RegOrgUnitsAuditTrail(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    org_unit = models.ForeignKey(RegOrgUnit)
    transaction_type_id = models.CharField(max_length=4, null=True,
                                           db_index=True)
    interface_id = models.CharField(max_length=4, null=True, db_index=True)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.ForeignKey(AppUser, db_column='user_id_modified')

    class Meta:
        db_table = 'reg_org_units_audit_trail'
        app_label = 'cpovc_registry'


class RegPersonsAuditTrail(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    person = models.ForeignKey(RegPerson)
    transaction_type_id = models.CharField(max_length=4, null=True,
                                           db_index=True)
    interface_id = models.CharField(max_length=4, null=True, db_index=True)
    date_recorded_paper = models.DateField(null=True)
    person_id_recorded_paper = models.IntegerField(null=True)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.ForeignKey(AppUser, db_column='user_id_modified')

    class Meta:
        db_table = 'reg_persons_audit_trail'
        app_label = 'cpovc_registry'
