# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import TheArtVillage.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surname', models.CharField(max_length=128)),
                ('firstname', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=16)),
                ('postcode', models.CharField(max_length=8, blank=True)),
                ('email', models.CharField(max_length=128)),
                ('fullname', models.CharField(max_length=256, editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Enter the name of the piece of art', max_length=128)),
                ('category', models.CharField(max_length=128)),
                ('sub_category', models.CharField(max_length=128)),
                ('price', TheArtVillage.models.MyDecimalField(max_digits=10, decimal_places=2)),
                ('quantity', models.IntegerField()),
                ('picture', models.ImageField(upload_to=TheArtVillage.models.generate_filename_art, blank=True)),
                ('slug', models.SlugField(max_length=160, editable=False, blank=True)),
                ('identification', models.CharField(max_length=10, editable=False, blank=True)),
                ('authenticate', models.CharField(max_length=64, editable=False, blank=True)),
                ('weight', models.CharField(help_text=b'weight in kg', max_length=16)),
                ('size', models.CharField(help_text=b'dimensions in cm', max_length=16)),
                ('description', models.TextField(blank=True)),
                ('artist', models.CharField(max_length=256, editable=False, blank=True)),
                ('agent', models.CharField(max_length=256, editable=False, blank=True)),
                ('special_delivery', models.BooleanField(default=False, help_text=b'check box if piece of art requires courier services (i.e. cannot be sent through mail)')),
                ('postage_price', TheArtVillage.models.MyDecimalField(help_text=b'Enter the price for postage in the UK, enter 0 if special delivery is required', max_digits=10, decimal_places=2)),
                ('agent_id', models.ForeignKey(help_text=b'Click magnifying glass to find correct agent', to='TheArtVillage.Agent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('surname', models.CharField(max_length=128)),
                ('firstname', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('fullname', models.CharField(max_length=256, editable=False, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, editable=False, blank=True)),
                ('additional_image', models.ImageField(upload_to=TheArtVillage.models.generate_filename_picture)),
                ('art', models.ForeignKey(help_text=b'Click magnifying glass to find correct piece of art', to='TheArtVillage.Art')),
            ],
            options={
                'ordering': ['additional_image'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='art',
            name='artist_id',
            field=models.ForeignKey(help_text=b'Click magnifying glass to find correct artist', to='TheArtVillage.Artist'),
            preserve_default=True,
        ),
    ]
