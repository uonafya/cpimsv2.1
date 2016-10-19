"""CPIMS OVC aggregate data models."""
from django.db import models
from django.utils import timezone


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
