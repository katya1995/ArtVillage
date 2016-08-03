# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0004_auto_20160729_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='town',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address1',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address2',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postcode',
            field=models.CharField(max_length=32, blank=True),
        ),
    ]
