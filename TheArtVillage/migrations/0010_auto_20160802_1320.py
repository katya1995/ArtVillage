# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import TheArtVillage.models


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0009_auto_20160802_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='art',
            name='postage_price',
            field=TheArtVillage.models.MyDecimalField(default=0.0, help_text=b'Enter the price for postage in the UK, enter 0 if special delivery is required', max_digits=10, decimal_places=2),
        ),
    ]
