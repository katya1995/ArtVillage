# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default=b'UK', max_length=5, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='postcode',
            field=models.CharField(default=b'', max_length=12, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='town',
            field=models.CharField(default=b'', max_length=28, blank=True),
            preserve_default=True,
        ),
    ]
