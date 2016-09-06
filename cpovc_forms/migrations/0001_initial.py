# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormsAuditTrail',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('form_id', models.UUIDField(null=True)),
                ('form_type_id', models.CharField(max_length=250)),
                ('transaction_type_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('interface_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('meta_data', models.TextField(null=True)),
            ],
            options={
                'db_table': 'forms_audit_trail',
            },
        ),
        migrations.CreateModel(
            name='FormsLog',
            fields=[
                ('form_log_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('form_type_id', models.CharField(max_length=250)),
                ('form_id', models.CharField(default=b'XXXX', max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('app_user', models.IntegerField(default=404, null=True)),
            ],
            options={
                'db_table': 'forms_log',
            },
        ),
        migrations.CreateModel(
            name='OVCAdverseEventsFollowUp',
            fields=[
                ('adverse_condition_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('adverse_condition_description', models.CharField(max_length=20)),
                ('adverse_event_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_adverseevents_followup',
            },
        ),
        migrations.CreateModel(
            name='OVCAdverseMedicalEventsFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adverse_medical_condition', models.CharField(max_length=20)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_adverse_medical_events_followup',
            },
        ),
        migrations.CreateModel(
            name='OVCBursary',
            fields=[
                ('bursary_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('bursary_type', models.CharField(max_length=4, null=True)),
                ('disbursement_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('amount', models.CharField(max_length=20, null=True)),
                ('year', models.CharField(max_length=20, null=True)),
                ('term', models.CharField(max_length=20, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('created_by', models.IntegerField(default=404, null=True)),
            ],
            options={
                'db_table': 'ovc_bursaryinfo',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseCategory',
            fields=[
                ('case_category_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('case_category', models.CharField(max_length=4)),
                ('case_grouping_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('date_of_event', models.DateField(default=django.utils.timezone.now)),
                ('place_of_event', models.CharField(max_length=4)),
                ('case_nature', models.CharField(max_length=4)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_category',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseEventClosure',
            fields=[
                ('closure_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('case_outcome', models.CharField(max_length=4)),
                ('date_of_case_closure', models.DateField(default=django.utils.timezone.now)),
                ('case_closure_notes', models.CharField(max_length=1000)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_event_closure',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseEventCourt',
            fields=[
                ('court_session_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('court_order', models.CharField(max_length=250, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_event_court',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseEvents',
            fields=[
                ('case_event_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('case_event_type_id', models.CharField(max_length=20)),
                ('date_of_event', models.DateField(default=django.utils.timezone.now)),
                ('case_event_details', models.CharField(max_length=100)),
                ('case_event_notes', models.CharField(max_length=1000, blank=True)),
                ('case_event_outcome', models.CharField(max_length=250, null=True)),
                ('next_hearing_date', models.DateField(null=True)),
                ('next_mention_date', models.DateField(null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_events',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseEventServices',
            fields=[
                ('service_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('service_provided', models.CharField(max_length=250)),
                ('service_provider', models.CharField(max_length=250, null=True)),
                ('place_of_service', models.CharField(max_length=250, null=True)),
                ('date_of_encounter_event', models.DateField(default=django.utils.timezone.now)),
                ('service_grouping_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_event_encounters',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseEventSummon',
            fields=[
                ('summon_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('honoured', models.BooleanField(default=False)),
                ('honoured_date', models.DateField(null=True)),
                ('summon_date', models.DateField(null=True)),
                ('summon_note', models.CharField(max_length=250, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_event_summon',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseGeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('report_ward', models.CharField(max_length=100, null=True)),
                ('report_village', models.CharField(max_length=100, null=True)),
                ('occurence_ward', models.CharField(max_length=100, blank=True)),
                ('occurence_village', models.CharField(max_length=100, blank=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_geo',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseRecord',
            fields=[
                ('case_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('case_serial', models.CharField(default=b'XXXX', max_length=50)),
                ('perpetrator_status', models.CharField(default=b'PKNW', max_length=20)),
                ('perpetrator_first_name', models.CharField(max_length=50, null=True)),
                ('perpetrator_other_names', models.CharField(max_length=50, null=True)),
                ('perpetrator_surname', models.CharField(max_length=50, null=True)),
                ('perpetrator_relationship_type', models.CharField(max_length=50, null=True)),
                ('risk_level', models.CharField(max_length=50)),
                ('date_case_opened', models.DateField(default=datetime.date.today)),
                ('case_reporter_first_name', models.CharField(max_length=50, null=True)),
                ('case_reporter_other_names', models.CharField(max_length=50, null=True)),
                ('case_reporter_surname', models.CharField(max_length=50, null=True)),
                ('case_reporter_contacts', models.CharField(max_length=20, null=True)),
                ('case_reporter', models.CharField(max_length=20, blank=True)),
                ('court_name', models.CharField(max_length=200, null=True)),
                ('court_number', models.CharField(max_length=50, null=True)),
                ('police_station', models.CharField(max_length=200, null=True)),
                ('ob_number', models.CharField(max_length=50, null=True)),
                ('case_status', models.CharField(default=b'ACTIVE', max_length=50)),
                ('referral_present', models.CharField(default=b'AYES', max_length=10)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('parent_case_id', models.UUIDField(null=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('case_remarks', models.CharField(max_length=1000, null=True)),
                ('date_of_summon', models.DateField(null=True)),
                ('summon_status', models.NullBooleanField(default=None)),
            ],
            options={
                'db_table': 'ovc_case_record',
            },
        ),
        migrations.CreateModel(
            name='OVCCaseSubCategory',
            fields=[
                ('case_sub_category_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('case_grouping_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('sub_category_id', models.CharField(max_length=4)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_case_sub_category',
            },
        ),
        migrations.CreateModel(
            name='OVCDischargeFollowUp',
            fields=[
                ('discharge_followup_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('type_of_discharge', models.CharField(max_length=20)),
                ('date_of_discharge', models.DateField(default=django.utils.timezone.now, null=True)),
                ('discharge_destination', models.CharField(max_length=20, null=True)),
                ('reason_of_discharge', models.CharField(max_length=1000, blank=True)),
                ('expected_return_date', models.DateField(null=True)),
                ('actual_return_date', models.DateField(null=True)),
                ('discharge_comments', models.CharField(max_length=1000, blank=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_discharge_followup',
            },
        ),
        migrations.CreateModel(
            name='OVCDocuments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_type', models.CharField(max_length=100)),
                ('document_description', models.CharField(max_length=200)),
                ('document_name', models.CharField(max_length=100, blank=True)),
                ('document_dir', models.CharField(max_length=1000, blank=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_documents',
            },
        ),
        migrations.CreateModel(
            name='OVCEconomicStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('household_economic_status', models.CharField(max_length=100)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_economic_status',
            },
        ),
        migrations.CreateModel(
            name='OVCEducationFollowUp',
            fields=[
                ('education_followup_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('admitted_to_school', models.CharField(max_length=10)),
                ('admission_to_school_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('education_comments', models.CharField(max_length=1000, null=True)),
                ('not_in_school_reason', models.CharField(max_length=4, null=True)),
                ('school_admission_type', models.CharField(max_length=4, null=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_education_followup',
            },
        ),
        migrations.CreateModel(
            name='OVCEducationLevelFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admission_level', models.CharField(max_length=20, null=True)),
                ('admission_sublevel', models.CharField(max_length=20, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_education_level_followup',
            },
        ),
        migrations.CreateModel(
            name='OVCFamilyCare',
            fields=[
                ('familycare_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('type_of_care', models.CharField(max_length=4)),
                ('certificate_number', models.CharField(max_length=20, null=True)),
                ('date_of_certificate_expiry', models.DateField(null=True)),
                ('type_of_adoption', models.CharField(max_length=4, null=True)),
                ('adoption_country', models.CharField(max_length=20, null=True)),
                ('date_of_adoption', models.DateField(default=django.utils.timezone.now, null=True)),
                ('court_name', models.CharField(max_length=100, null=True)),
                ('court_file_number', models.CharField(max_length=20, null=True)),
                ('parental_status', models.CharField(max_length=4, null=True)),
                ('contact_person', models.CharField(max_length=20, null=True)),
                ('adopting_mother_firstname', models.CharField(max_length=20, null=True)),
                ('adopting_mother_surname', models.CharField(max_length=20, null=True)),
                ('adopting_mother_othernames', models.CharField(max_length=20, null=True)),
                ('adopting_mother_idnumber', models.CharField(max_length=20, null=True)),
                ('adopting_mother_contacts', models.CharField(max_length=20, null=True)),
                ('adopting_father_firstname', models.CharField(max_length=20, null=True)),
                ('adopting_father_surname', models.CharField(max_length=20, null=True)),
                ('adopting_father_othernames', models.CharField(max_length=20, null=True)),
                ('adopting_father_idnumber', models.CharField(max_length=20, null=True)),
                ('adopting_father_contacts', models.CharField(max_length=20, null=True)),
                ('adopting_agency', models.CharField(max_length=20, null=True)),
                ('adoption_remarks', models.CharField(max_length=1000, null=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_family_care',
            },
        ),
        migrations.CreateModel(
            name='OVCFamilyStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('family_status', models.CharField(max_length=100)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_family_status',
            },
        ),
        migrations.CreateModel(
            name='OVCFriends',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friend_firstname', models.CharField(max_length=50)),
                ('friend_other_names', models.CharField(max_length=50)),
                ('friend_surname', models.CharField(max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_friends',
            },
        ),
        migrations.CreateModel(
            name='OVCHobbies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hobby', models.CharField(max_length=200)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_hobbies',
            },
        ),
        migrations.CreateModel(
            name='OVCMedical',
            fields=[
                ('medical_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('mental_condition', models.CharField(max_length=50)),
                ('physical_condition', models.CharField(max_length=50)),
                ('other_condition', models.CharField(max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_medical',
            },
        ),
        migrations.CreateModel(
            name='OVCMedicalSubconditions',
            fields=[
                ('medicalsubcond_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('medical_condition', models.CharField(max_length=50)),
                ('medical_subcondition', models.CharField(max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_medical_subconditions',
            },
        ),
        migrations.CreateModel(
            name='OVCNeeds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('need_description', models.CharField(max_length=250)),
                ('need_type', models.CharField(max_length=250)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_needs',
            },
        ),
        migrations.CreateModel(
            name='OVCPlacement',
            fields=[
                ('placement_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('residential_institution_name', models.CharField(max_length=100, blank=True)),
                ('admission_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('admission_type', models.CharField(max_length=4, blank=True)),
                ('transfer_from', models.CharField(max_length=100, null=True)),
                ('admission_reason', models.CharField(max_length=100, blank=True)),
                ('holding_period', models.IntegerField(null=True)),
                ('committing_period_units', models.CharField(max_length=4, null=True)),
                ('committing_period', models.IntegerField(null=True)),
                ('current_residential_status', models.CharField(max_length=4)),
                ('has_court_committal_order', models.CharField(max_length=4)),
                ('free_for_adoption', models.CharField(max_length=4, null=True)),
                ('court_order_number', models.CharField(max_length=20, null=True)),
                ('court_order_issue_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('committing_court', models.CharField(max_length=100, null=True)),
                ('placement_notes', models.CharField(max_length=1000, null=True)),
                ('ob_number', models.CharField(max_length=20, null=True)),
                ('placement_type', models.CharField(default=b'Normal', max_length=10)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_placement',
            },
        ),
        migrations.CreateModel(
            name='OVCPlacementFollowUp',
            fields=[
                ('placememt_followup_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('followup_type', models.CharField(max_length=100)),
                ('followup_date', models.DateField(default=django.utils.timezone.now)),
                ('followup_details', models.CharField(max_length=1000, blank=True)),
                ('followup_outcome', models.CharField(max_length=1000, blank=True)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_placement_followup',
            },
        ),
        migrations.CreateModel(
            name='OVCReferral',
            fields=[
                ('refferal_id', models.UUIDField(default=uuid.uuid1, serialize=False, editable=False, primary_key=True)),
                ('refferal_actor_type', models.CharField(max_length=4)),
                ('refferal_actor_specify', models.CharField(max_length=50)),
                ('refferal_to', models.CharField(max_length=4)),
                ('refferal_status', models.CharField(default=b'PENDING', max_length=20)),
                ('refferal_startdate', models.DateField(default=datetime.date.today)),
                ('refferal_enddate', models.DateField(null=True)),
                ('referral_grouping_id', models.UUIDField(default=uuid.uuid1, editable=False)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_referrals',
            },
        ),
        migrations.CreateModel(
            name='OVCReminders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reminder_date', models.DateField(default=django.utils.timezone.now)),
                ('reminder_type', models.CharField(max_length=100)),
                ('reminder_description', models.CharField(max_length=1000)),
                ('reminder_status', models.CharField(max_length=10)),
                ('created_by', models.IntegerField(default=404, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_reminders',
            },
        ),
    ]
