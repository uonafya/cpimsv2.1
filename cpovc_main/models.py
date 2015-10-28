from django.db import models
from django.utils import timezone
from cpovc_registry.models import RegPerson


class AdminPreferences(models.Model):
    person = models.ForeignKey(RegPerson)
    preference_id = models.CharField(max_length=4)

    class Meta:
        db_table = 'admin_preferences'


class CoreAdverseConditions(models.Model):
    beneficiary_person = models.ForeignKey(RegPerson)
    adverse_condition_id = models.CharField(max_length=4)
    is_void = models.BooleanField(default=False)
    sms_id = models.IntegerField(null=True)
    form_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'core_adverse_conditions'


class CoreServices(models.Model):
    workforce_person = models.ForeignKey(RegPerson,
                                         related_name='service_workforce')
    beneficiary_person = models.ForeignKey(RegPerson,
                                           related_name='service_beneficiary')
    encounter_date = models.DateField()
    core_item_id = models.CharField(max_length=4)
    sms_id = models.IntegerField(null=True)
    form_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'core_services'


class CoreEncounters(models.Model):
    workforce_person = models.ForeignKey(RegPerson,
                                         related_name='encounter_workforce')
    beneficiary_person = models.ForeignKey(RegPerson,
                                           related_name='encouner_beneficiary')
    encounter_date = models.DateField()
    org_unit_id = models.IntegerField()
    area_id = models.IntegerField()
    encounter_type_id = models.CharField(max_length=4)
    sms_id = models.IntegerField(null=True)
    form_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'core_encounters'
        # unique_together = ("workforce_person", "beneficiary_person",
        # "encounter_date", "form_id")


class CoreEncountersNotes(models.Model):
    encounter = models.ForeignKey(CoreEncounters)
    form_id = models.IntegerField()
    workforce_person = models.ForeignKey(RegPerson,
                                         related_name='encounter_n_workforce')
    beneficiary_person = models.ForeignKey(
        RegPerson, related_name='encouner_n_beneficiary')
    encounter_date = models.DateField()
    note_type_id = models.CharField(max_length=4)
    note = models.CharField(max_length=255)

    class Meta:
        db_table = 'form_encounters_notes'


class AdminCaptureSites(models.Model):
    org_unit_id = models.IntegerField(null=True)
    capture_site_name = models.CharField(max_length=255, null=True, blank=True)
    date_installed = models.DateField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'admin_capture_sites'


class Forms(models.Model):
    form_guid = models.CharField(max_length=64)
    form_title = models.CharField(max_length=255, null=True)
    form_type_id = models.CharField(max_length=4, null=True)
    form_subject_id = models.IntegerField(null=True, blank=False)
    form_area_id = models.IntegerField(null=True)
    date_began = models.DateField(null=True)
    date_ended = models.DateField(null=True)
    date_filled_paper = models.DateField(null=True)
    person_id_filled_paper = models.IntegerField(null=True)
    org_unit_id_filled_paper = models.IntegerField(null=True)
    capture_site_id = models.IntegerField(null=True, blank=True)
    timestamp_created = models.DateTimeField(null=True)
    user_id_created = models.CharField(max_length=9, null=True)
    timestamp_updated = models.DateTimeField(null=True)
    user_id_updated = models.CharField(max_length=9, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'forms'


class AdminDownload(models.Model):
    capture_site_id = models.IntegerField(null=True, blank=True)
    section_id = models.CharField(max_length=4, null=True)
    timestamp_started = models.DateTimeField(null=True)
    timestamp_completed = models.DateTimeField(null=True)
    number_records = models.IntegerField(null=True)
    request_id = models.CharField(max_length=64, null=True)
    success = models.BooleanField(default=False)

    class Meta:
        db_table = 'admin_download'


class AdminUploadForms(models.Model):
    form = models.ForeignKey(Forms)
    timestamp_uploaded = models.DateTimeField(null=True)

    class Meta:
        db_table = 'admin_upload_forms'


class ListQuestions(models.Model):
    question_text = models.CharField(max_length=255, null=True, blank=True)
    question_code = models.CharField(max_length=50)
    form_type_id = models.CharField(max_length=4, null=True, blank=True)
    answer_type_id = models.CharField(max_length=4, null=True, blank=True)
    answer_set_id = models.IntegerField(db_index=True, null=True)
    the_order = models.IntegerField(db_index=True, null=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'list_questions'


class ListAnswers(models.Model):
    answer_set_id = models.IntegerField(db_index=True, null=True)
    answer = models.CharField(max_length=255, null=True, blank=True)
    the_order = models.IntegerField(db_index=True, null=True)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True)
    is_void = models.BooleanField(default=False)

    class Meta:
        db_table = 'list_answers'


class FormGenAnswers(models.Model):
    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer = models.ForeignKey(ListAnswers, null=True)

    class Meta:
        db_table = 'form_gen_answers'


class FormGenText(models.Model):
    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer_text = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'form_gen_text'


class FormGenDates(models.Model):
    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer_date = models.DateField()

    class Meta:
        db_table = 'form_gen_dates'


class FormGenNumeric(models.Model):
    form = models.ForeignKey(Forms)
    question = models.ForeignKey(ListQuestions)
    answer = models.DecimalField(null=True, decimal_places=1, max_digits=10)

    class Meta:
        db_table = 'form_gen_numeric'


class FormCsi(models.Model):
    form = models.ForeignKey(Forms)
    domain_id = models.CharField(max_length=4, null=True, blank=True)
    # TODO part of composite key for domain_id
    score = models.IntegerField(null=True, blank=True)
    observations = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'form_csi'


class FormPersonParticipation(models.Model):
    form = models.ForeignKey(Forms)
    workforce_or_beneficiary_id = models.CharField(max_length=15)
    participation_level_id = models.CharField(max_length=4, null=True,
                                              blank=True)

    class Meta:
        db_table = 'form_person_participation'


class FormOrgUnitContributions(models.Model):
    form = models.ForeignKey(Forms)
    org_unit_id = models.CharField(max_length=7)
    contribution_id = models.CharField(max_length=4)
    # TODO part of composite key - org_unit_id and contrib_id

    class Meta:
        db_table = 'form_org_unit_contribution'


class FormResChildren(models.Model):
    form = models.ForeignKey(Forms, null=True)
    child_person_id = models.IntegerField(null=True, blank=True)
    institution_id = models.IntegerField(null=True, blank=True)
    residential_status_id = models.CharField(max_length=4, null=True,
                                             blank=True)
    court_committal_id = models.CharField(max_length=4, null=True, blank=True)
    family_status_id = models.CharField(max_length=4, null=True, blank=True)
    date_admitted = models.DateField(null=True, blank=True)
    date_left = models.DateField(null=True, blank=True)
    sms_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'form_res_children'


class FormResWorkforce(models.Model):
    form = models.ForeignKey(Forms)
    workforce_id = models.IntegerField(null=True, blank=True)
    institution_id = models.IntegerField(null=True, blank=True)
    position_id = models.CharField(max_length=4, null=True, blank=True)
    full_part_time_id = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        db_table = 'form_res_workforce'


class CaptureTaskTracker(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=64, null=True)
    operation = models.CharField(max_length=8, null=True)
    timestamp_started = models.DateTimeField(auto_now=True,
                                             default=timezone.now)
    timestamp_completed = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    class Meta:
        db_table = 'admin_task_tracker'


class ListReports(models.Model):
    report_code = models.CharField(max_length=100, null=True, blank=True)
    report_title_short = models.CharField(max_length=255, null=True)
    report_title_long = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'list_reports'


class ListReportsParameters(models.Model):
    report = models.ForeignKey(ListReports, null=True)
    parameter = models.CharField(max_length=50, null=True, blank=True)
    filter = models.CharField(max_length=50, null=True, blank=True)
    initially_visible = models.BooleanField(default=False)
    label = models.CharField(max_length=100, null=True, blank=True)
    tip = models.CharField(max_length=255, null=True, blank=True)
    required = models.BooleanField(default=False)

    class Meta:
        db_table = 'list_reports_parameter'


class ReportsSets(models.Model):
    set_name = models.CharField(max_length=70)
    set_type_id = models.CharField(max_length=4, default='SORG')
    user_id_created = models.IntegerField()

    class Meta:
        db_table = 'reports_sets'


class ReportsSetsOrgUnits(models.Model):
    set = models.ForeignKey(ReportsSets)
    org_unit_id = models.IntegerField()

    class Meta:
        db_table = 'reports_sets_org_unit'
        unique_together = ("set", "org_unit_id")
