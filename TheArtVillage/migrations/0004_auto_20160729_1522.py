# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0003_auto_20160729_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='address1',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address2',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='postcode',
            field=models.CharField(max_length=12, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='town',
            field=models.CharField(max_length=28, blank=True),
        ),
    ]
