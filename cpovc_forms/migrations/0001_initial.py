# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCCaseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_event', models.CharField(max_length=50)),
                ('place_of_event', models.CharField(max_length=50)),
                ('perpetrator_first_name', models.CharField(max_length=50)),
                ('perpetrator_other_names', models.CharField(max_length=50)),
                ('perpetrator_surname', models.CharField(max_length=50)),
                ('relationship_type_id', models.CharField(max_length=50)),
                ('case_type', models.CharField(max_length=100)),
                ('case_nature', models.CharField(max_length=100)),
                ('intervention', models.CharField(max_length=50)),
                ('risk_level', models.CharField(max_length=50)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_case_record',
            },
        ),
        migrations.CreateModel(
            name='OVCDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('religion', models.CharField(max_length=100)),
                ('tribe', models.CharField(max_length=100)),
                ('child_in_school', models.CharField(max_length=100)),
                ('family_status_id', models.CharField(max_length=100)),
                ('household_economic_status', models.CharField(max_length=100)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_secondary_details',
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
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_friends',
            },
        ),
        migrations.CreateModel(
            name='OVCHobbies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hobby_id', models.CharField(max_length=20)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_hobbies',
            },
        ),
        migrations.CreateModel(
            name='OVCMedical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mental_condition', models.CharField(max_length=50)),
                ('physical_condition', models.CharField(max_length=50)),
                ('other_condition', models.CharField(max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_medical',
            },
        ),
        migrations.CreateModel(
            name='OVCNeeds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('need_description', models.CharField(max_length=250)),
                ('need_type', models.CharField(max_length=250)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_needs',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('school_name', models.CharField(max_length=100)),
                ('class_level', models.CharField(default=None, max_length=50)),
                ('school_category_id', models.CharField(max_length=50)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_school',
            },
        ),
        migrations.CreateModel(
            name='Sibling',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('other_names', models.CharField(default=None, max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('sex_id', models.CharField(max_length=4)),
                ('class_level', models.IntegerField(null=True)),
                ('remarks', models.CharField(max_length=1000, null=True)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('timestamp_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='cpovc_registry.RegPerson')),
            ],
            options={
                'db_table': 'ovc_sibling',
            },
        ),
    ]
