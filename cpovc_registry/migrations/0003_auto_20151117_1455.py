# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0002_auto_20151117_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regperson',
            name='beneficiary_id',
        ),
        migrations.RemoveField(
            model_name='regperson',
            name='birth_reg_id',
        ),
        migrations.RemoveField(
            model_name='regperson',
            name='national_id',
        ),
        migrations.RemoveField(
            model_name='regperson',
            name='staff_id',
        ),
        migrations.RemoveField(
            model_name='regperson',
            name='workforce_id',
        ),
    ]
