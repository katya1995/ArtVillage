# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('TheArtVillage', '0007_auto_20160801_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payer_email', models.CharField(max_length=128)),
                ('time', models.CharField(max_length=128)),
                ('payment_date', models.DateField(max_length=128)),
                ('payment_gross', models.FloatField(max_length=128)),
                ('payment_fee', models.FloatField(max_length=128)),
                ('payment_net', models.FloatField(max_length=128)),
                ('payment_status', models.BooleanField()),
                ('buyer', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
