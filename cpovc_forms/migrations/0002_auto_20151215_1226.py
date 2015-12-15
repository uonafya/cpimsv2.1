# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpovc_registry', '0001_initial'),
        ('cpovc_forms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sibling',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='school',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcneeds',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcmedical',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovchobbies',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcfriends',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovcdetails',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
        migrations.AddField(
            model_name='ovccaserecord',
            name='person',
            field=models.ForeignKey(to='cpovc_registry.RegPerson'),
        ),
    ]
