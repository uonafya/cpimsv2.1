# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RegOrgUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('org_unit_id_vis', models.CharField(max_length=12)),
                ('org_unit_name', models.CharField(max_length=255)),
                ('org_unit_type_id', models.CharField(max_length=4)),
                ('date_operational', models.DateField(null=True)),
                ('date_closed', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('parent_org_unit_id', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'reg_org_unit',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_detail_type_id', models.CharField(max_length=20)),
                ('contact_detail', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_contact',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitExternalID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier_type_id', models.CharField(max_length=4)),
                ('identifier_value', models.CharField(max_length=255, null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_external_ids',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitGeography',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('area', models.ForeignKey(to='cpovc_main.SetupGeography')),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_geo',
            },
        ),
        migrations.CreateModel(
            name='RegOrgUnitsAuditTrail',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_type_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('interface_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('app_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'user_id_modified')),
                ('org_unit', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
            ],
            options={
                'db_table': 'reg_org_units_audit_trail',
            },
        ),
        migrations.CreateModel(
            name='RegPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation', models.CharField(default=None, max_length=25)),
                ('first_name', models.CharField(max_length=255)),
                ('other_names', models.CharField(default=None, max_length=255)),
                ('surname', models.CharField(default=None, max_length=255)),
                ('email', models.EmailField(default=None, max_length=254, blank=True)),
                ('des_phone_number', models.IntegerField(default=None, null=True)),
                ('date_of_birth', models.DateField()),
                ('date_of_death', models.DateField(default=None, null=True, blank=True)),
                ('sex_id', models.CharField(max_length=4)),
                ('is_void', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'reg_person',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsAuditTrail',
            fields=[
                ('transaction_id', models.AutoField(serialize=False, primary_key=True)),
                ('transaction_type_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('interface_id', models.CharField(max_length=4, null=True, db_index=True)),
                ('date_recorded_paper', models.DateField(null=True)),
                ('person_id_recorded_paper', models.IntegerField(null=True)),
                ('timestamp_modified', models.DateTimeField(auto_now=True)),
                ('app_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'user_id_modified')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_audit_trail',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsBeneficiaryIds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficiary_id', models.CharField(max_length=10, null=True)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_beneficiary_ids',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_detail_type_id', models.CharField(max_length=4)),
                ('contact_detail', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_contact',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsExternalIds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier_type_id', models.CharField(max_length=4)),
                ('identifier', models.CharField(max_length=255)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_external_ids',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsGeo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('area', models.ForeignKey(to='cpovc_main.SetupGeography')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_geo',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsGuardians',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guardian_person_id', models.CharField(max_length=255)),
                ('relationship', models.CharField(max_length=255)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('child_person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_guardians',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsOrgUnits',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_linked', models.DateField(null=True)),
                ('date_delinked', models.DateField(null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('org_unit_id', models.ForeignKey(to='cpovc_registry.RegOrgUnit')),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_org_units',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person_type_id', models.CharField(max_length=4)),
                ('date_began', models.DateField(null=True)),
                ('date_ended', models.DateField(default=None, null=True)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_types',
            },
        ),
        migrations.CreateModel(
            name='RegPersonsWorkforceIds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('workforce_id', models.CharField(max_length=8, null=True)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'reg_persons_workforce_ids',
            },
        ),
    ]
