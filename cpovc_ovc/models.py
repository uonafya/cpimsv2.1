"""CPIMS OVC aggregate data models."""
import uuid
from django.db import models
from django.utils import timezone
from cpovc_registry.models import RegPerson, RegOrgUnit


class OVCAggregate(models.Model):
    """Model for Organisational Units details."""

    indicator_name = models.CharField(max_length=100, null=False)
    project_year = models.IntegerField(null=False)
    reporting_period = models.CharField(max_length=50, null=False)
    cbo = models.CharField(max_length=255, null=False)
    subcounty = models.CharField(max_length=100, null=False)
    county = models.CharField(max_length=100, null=False)
    ward = models.CharField(max_length=100, null=False)
    implementing_partnerid = models.IntegerField(null=False)
    implementing_partner = models.CharField(max_length=200, null=False)
    indicator_count = models.IntegerField(null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=50, null=False)
    county_active = models.IntegerField(null=False)
    subcounty_active = models.IntegerField(null=False)
    ward_active = models.IntegerField(null=False)
    created_at = models.DateField(null=True, default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'ovc_aggregate'
        verbose_name = 'OVC aggregate data'
        verbose_name_plural = 'OVC aggregate data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.indicator_name


class OVCUpload(models.Model):
    """Model for Organisational Units details."""

    implementing_partnerid = models.IntegerField(null=False)
    project_year = models.IntegerField(null=False)
    reporting_period = models.CharField(max_length=50, null=False)
    ovc_filename = models.CharField(max_length=255, null=False)
    created_at = models.DateField(null=True, default=timezone.now)

    class Meta:
        """Override table details."""

        db_table = 'ovc_upload'
        verbose_name = 'OVC upload data'
        verbose_name_plural = 'OVC upload data'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.ovc_filename


class OVCRegistration(models.Model):
    """Model for Organisational Units details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson, null=False)
    registration_date = models.DateField(default=timezone.now)
    has_bcert = models.BooleanField(null=False, default=False)
    is_disabled = models.BooleanField(null=False, default=False)
    hiv_status = models.CharField(max_length=4, null=True)
    school_level = models.CharField(max_length=4, null=True)
    immunization_status = models.CharField(max_length=4, null=True)
    org_unique_id = models.CharField(max_length=15, null=True)
    caretaker = models.ForeignKey(RegPerson, null=True, related_name='ctaker')
    child_cbo = models.ForeignKey(RegOrgUnit)
    child_chv = models.ForeignKey(RegPerson, related_name='chv')
    exit_date = models.DateField(default=timezone.now, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'ovc_registration'
        verbose_name = 'OVC Registration'
        verbose_name_plural = 'OVC Registration'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.org_unique_id


class OVCHouseHold(models.Model):
    """Model for Organisational Units details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    head_person = models.ForeignKey(RegPerson)
    head_identifier = models.CharField(max_length=15)
    created_at = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'ovc_household'
        verbose_name = 'OVC Registration'
        verbose_name_plural = 'OVC Registration'

    def __unicode__(self):
        """To be returned by admin actions."""
        return str(self.id)


class OVCHHMembers(models.Model):
    """Model for Organisational Units details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    house_hold = models.ForeignKey(OVCHouseHold, default=uuid.uuid4)
    person = models.ForeignKey(RegPerson)
    hh_head = models.BooleanField(default=False)
    member_type = models.CharField(max_length=4)
    death_cause = models.CharField(max_length=4, null=True)
    hiv_status = models.CharField(max_length=4, null=True)
    date_linked = models.DateField(default=timezone.now)
    date_delinked = models.DateField(null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'ovc_household_members'
        verbose_name = 'OVC Registration'
        verbose_name_plural = 'OVC Registration'

    def __unicode__(self):
        """To be returned by admin actions."""
        return self.id


class OVCHealth(models.Model):
    """Model for OVC Care health details."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(RegPerson)
    facility = models.ForeignKey(RegOrgUnit)
    art_status = models.CharField(max_length=4)
    date_linked = models.DateField()
    ccc_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        """Override table details."""

        db_table = 'ovc_care_health'
        verbose_name = 'OVC Care Health'
        verbose_name_plural = 'OVC Care Health'

    def __unicode__(self):
        """To be returned by admin actions."""
        return str(self.id)
