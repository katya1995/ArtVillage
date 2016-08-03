# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0005_auto_20160730_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='surname',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=5, blank=True),
        ),
    ]
