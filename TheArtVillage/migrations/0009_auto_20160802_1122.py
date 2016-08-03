# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TheArtVillage', '0008_orders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
