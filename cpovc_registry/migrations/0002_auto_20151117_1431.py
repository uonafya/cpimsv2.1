# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='regperson',
            name='staff_id',
            field=models.CharField(default=None, max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='regpersonstypes',
            name='date_ended',
            field=models.DateField(default=None, null=True),
        ),
    ]
