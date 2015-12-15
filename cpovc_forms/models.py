from django.db import models
from django.utils import timezone
from cpovc_registry.models import RegPerson


# Create your models here.
class Sibling(models.Model):
    first_name = models.CharField(max_length=50)
    other_names = models.CharField(max_length=50, default=None)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    sex_id = models.CharField(max_length=4)
    class_level = models.IntegerField(null=True)
    remarks = models.CharField(max_length=1000, null=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_sibling'


class School(models.Model):
    school_name = models.CharField(max_length=100)
    class_level = models.CharField(max_length=50, default=None)
    school_category_id = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_school'


class OVCDetails(models.Model):
    religion = models.CharField(max_length=100)
    tribe = models.CharField(max_length=100)
    child_in_school = models.CharField(max_length=100)
    family_status_id = models.CharField(max_length=100)
    household_economic_status = models.CharField(max_length=100)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_secondary_details'


class OVCHobbies(models.Model):
    hobby_id = models.CharField(max_length=20)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_hobbies'


class OVCFriends(models.Model):
    friend_firstname = models.CharField(max_length=50)
    friend_other_names = models.CharField(max_length=50)
    friend_surname = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_friends'


class OVCMedical(models.Model):
    mental_condition = models.CharField(max_length=50)
    physical_condition = models.CharField(max_length=50)
    other_condition = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_medical'


class OVCCaseRecord(models.Model):
    date_of_event = models.CharField(max_length=50)
    place_of_event = models.CharField(max_length=50)
    perpetrator_first_name = models.CharField(max_length=50)
    perpetrator_other_names = models.CharField(max_length=50)
    perpetrator_surname = models.CharField(max_length=50)
    relationship_type_id = models.CharField(max_length=50)
    case_type = models.CharField(max_length=100)
    case_nature = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=50)
    intervention = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=50)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_case_record'


class OVCNeeds(models.Model):
    need_description = models.CharField(max_length=250)
    need_type = models.CharField(max_length=250)
    # LongTerm/Immediate
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_needs'
