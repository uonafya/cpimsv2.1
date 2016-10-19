# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_forms', '0002_auto_20160812_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='OVCAdverseEventsOtherFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adverse_condition', models.CharField(max_length=20)),
                ('timestamp_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_void', models.BooleanField(default=False)),
                ('sync_id', models.UUIDField(default=uuid.uuid1, editable=False)),
            ],
            options={
                'db_table': 'ovc_adverseevents_other_followup',
            },
        ),
        migrations.RemoveField(
            model_name='ovcadversemedicaleventsfollowup',
            name='adverse_condition_id',
        ),
        migrations.AddField(
            model_name='ovcadverseeventsfollowup',
            name='attendance_type',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='ovcadverseeventsfollowup',
            name='referral_type',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='application_outcome',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='ovccaseevents',
            name='plea_taken',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.DeleteModel(
            name='OVCAdverseMedicalEventsFollowUp',
        ),
        migrations.AddField(
            model_name='ovcadverseeventsotherfollowup',
            name='adverse_condition_id',
            field=models.ForeignKey(to='cpovc_forms.OVCAdverseEventsFollowUp'),
        ),
    ]
