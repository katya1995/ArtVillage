# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0002_auto_20160729_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address1',
            field=models.CharField(default=b'', max_length=128, blank=b'True'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address2',
            field=models.CharField(default=b'', max_length=128, blank=b'True'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(default=b'UK', max_length=5),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='town',
            field=models.CharField(default=b'', max_length=28),
        ),
    ]
