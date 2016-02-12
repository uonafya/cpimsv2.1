from django.db import models
from django.utils import timezone
import uuid
from cpovc_registry.models import (RegPerson, RegOrgUnit, AppUser)

# Create your models here.


class OVCCaseRecord(models.Model):
    # Make case_id primary key
    case_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    case_serial = models.CharField(max_length=20, default='XXXX')
    place_of_event = models.CharField(max_length=50)
    perpetrator_first_name = models.CharField(max_length=50)
    perpetrator_other_names = models.CharField(max_length=50)
    perpetrator_surname = models.CharField(max_length=50)
    perpetrator_relationship_type = models.CharField(max_length=50)
    case_nature = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=50)
    date_case_opened = models.DateTimeField(default=timezone.now)
    case_reporter_first_name = models.CharField(max_length=50, blank=True)
    case_reporter_other_names = models.CharField(max_length=50, blank=True)
    case_reporter_surname = models.CharField(max_length=50, blank=True)
    case_reporter_contacts = models.CharField(max_length=20, blank=True)
    case_reporter_relationship_to_child = models.CharField(
        max_length=100, blank=True)
    case_status = models.CharField(max_length=50, default='ACTIVE')
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)
    case_remarks = models.CharField(max_length=1000, blank=True)

    class Meta:
        db_table = 'ovc_case_record'


class OVCDetails(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord)
    family_status_id = models.CharField(max_length=100)
    household_economic_status = models.CharField(max_length=100)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_secondary_details'


class OVCHobbies(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord)
    hobby = models.CharField(max_length=200)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_hobbies'


class OVCFriends(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord)
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
    case_id = models.ForeignKey(OVCCaseRecord)
    mental_condition = models.CharField(max_length=50)
    physical_condition = models.CharField(max_length=50)
    other_condition = models.CharField(max_length=50)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_medical'


class OVCCaseCategory(models.Model):
    case_category_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    #case_category_id = models.CharField(max_length=10, primary_key=True)
    case_id = models.ForeignKey(OVCCaseRecord)
    case_category = models.CharField(max_length=100)
    case_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    date_of_event = models.DateField(default=timezone.now)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_case_category'


class OVCInterventions(models.Model):
    inteventions_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    intervention = models.CharField(max_length=100)
    case_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_case_interventions'


class OVCReferral(models.Model):
    refferal_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    refferal_destination_type = models.CharField(max_length=20, default='XXXX')
    refferal_to = models.CharField(max_length=200)
    refferal_reason = models.CharField(max_length=1000, default='XXXX')
    refferal_status = models.CharField(max_length=10, default='PENDING')
    date_of_referral_event = models.DateField(null=True)
    case_grouping_id = models.UUIDField(default=uuid.uuid1, editable=False)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_refferals'


class OVCNeeds(models.Model):
    case_id = models.ForeignKey(OVCCaseRecord)
    need_description = models.CharField(max_length=250)
    need_type = models.CharField(max_length=250)  # LongTerm/Immediate
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    person = models.ForeignKey(RegPerson)

    class Meta:
        db_table = 'ovc_needs'


class FormsAuditTrail(models.Model):
    form_type_id = models.CharField(max_length=250)
    form_id = models.CharField(max_length=50, default='XXXX')
    person = models.ForeignKey(RegPerson)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    timestamp_modified = models.DateTimeField(auto_now=True)
    app_user = models.IntegerField(null=True, default=404)
    # app_user = models.ForeignKey(AppUser, default=1)

    class Meta:
        db_table = 'forms_audit_trail'


class OVCCaseEvents(models.Model):
    case_event_id = models.CharField(primary_key=True, max_length=25)
    case_event_type_id = models.CharField(max_length=250)
    date_of_event = models.DateField(default=timezone.now)
    case_event_details = models.CharField(max_length=100)
    case_event_notes = models.CharField(max_length=1000, blank=True)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)
    case_id = models.ForeignKey(OVCCaseRecord)
    #app_user = models.IntegerField(null=True, default=404)
    app_user = models.ForeignKey(AppUser, default=1)

    class Meta:
        db_table = 'ovc_case_events'


class OVCCaseEventServices(models.Model):
    # Encounters/Services
    service_provided = models.CharField(max_length=250)
    case_event_id = models.ForeignKey(OVCCaseEvents)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    case_category_id = models.ForeignKey(OVCCaseCategory)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_case_event_encounters'


class OVCCaseEventCourt(models.Model):
    court_order = models.CharField(max_length=250)
    case_event_id = models.ForeignKey(OVCCaseEvents)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    case_category_id = models.ForeignKey(OVCCaseCategory)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_case_event_court'


class OVCCaseEventPlacement(models.Model):
    residential_institution = models.ForeignKey(RegOrgUnit) # org_unit_id_vis
    current_residential_status = models.CharField(max_length=250)
    has_court_committal_order = models.CharField(max_length=10)
    free_for_adoption = models.CharField(max_length=10)
    admission_date = models.DateField(default=timezone.now)
    departure_date = models.DateField(null=True)
    case_event_id = models.ForeignKey(OVCCaseEvents)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    case_category_id = models.ForeignKey(OVCCaseCategory)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_case_event_placement'


class OVCCaseClosure(models.Model):
    case_status = models.CharField(max_length=250)
    case_outcome_notes = models.CharField(max_length=1000)
    date_of_case_closure = models.DateField(default=timezone.now)
    case_id = models.ForeignKey(OVCCaseRecord)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_case_closure'


class OVCReminders(models.Model):
    reminder_date = models.DateField(default=timezone.now)
    reminder_type = models.CharField(max_length=100)
    reminder_description = models.CharField(max_length=1000)
    reminder_status = models.CharField(max_length=10)
    person = models.ForeignKey(RegPerson)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_reminders'


class OVCDocuments(models.Model):
    document_type = models.CharField(max_length=100)
    document_description = models.CharField(max_length=200)
    document_name = models.CharField(max_length=100, blank=True)
    document_dir = models.CharField(max_length=1000, blank=True)
    person = models.ForeignKey(RegPerson)
    timestamp_created = models.DateTimeField(default=timezone.now)
    timestamp_updated = models.DateTimeField(default=timezone.now)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'ovc_documents'
