# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dj', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0001_initial'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=1000, verbose_name=b'Description', blank=True)),
                ('name', models.CharField(max_length=140, verbose_name=b'Name of the nightclub')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Official email address for the club')),
                ('website', models.URLField(max_length=256, verbose_name=b'Official Club Website', blank=True)),
                ('facebook_page', models.URLField(max_length=256, verbose_name=b'Link to Facebook Page', blank=True)),
                ('city', models.CharField(help_text=b'What city is the club based in?', max_length=70, verbose_name=b'City')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('cost', models.CharField(default=b'med', max_length=3, blank=True, choices=[(b'low', b'$'), (b'med', b'$$'), (b'exp', b'$$$')])),
                ('cover_charge', models.NullBooleanField(default=False, verbose_name=b'Cover Charge')),
                ('live_music', models.NullBooleanField(verbose_name=b'Live Music')),
                ('dress_code', models.PositiveSmallIntegerField(default=1, blank=True, choices=[(1, b'Chilled'), (2, b'Formal'), (3, b'Fancy')])),
                ('style', models.PositiveSmallIntegerField(default=0, blank=True, choices=[(0, b'Chilled'), (1, b'Lounge'), (2, b'Dance Floor'), (3, b'Hipster'), (4, b'Sports Bar')])),
                ('uses_partysense', models.BooleanField(default=False, verbose_name=b'Uses Partysense')),
                ('live_on_partysense', models.BooleanField(default=False, verbose_name=b'Live on Partysense')),
                ('admins', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('djs', models.ManyToManyField(to='dj.DJ')),
                ('genres', models.ManyToManyField(to='music.Genre')),
                ('location', models.ForeignKey(verbose_name=b'Where is the club?', to='event.Location')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
