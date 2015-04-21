# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text=b'Keep it simple', max_length=70, verbose_name=b'Event Name')),
                ('description', models.TextField(help_text=b'Guidance to attendees about what to expect.\n    <strong>Eg:</strong>\n    <blockquote>We will play any tracks with more than 10 up votes</blockquote>\n\n    ', verbose_name=b'Event Description', blank=True)),
                ('past_event', models.BooleanField(default=False, editable=False)),
                ('user_editable', models.BooleanField(default=True, help_text=b'If not selected, only Event DJs can add songs to the playlist.\n                                        Other users will still be able to vote on the music you have chosen.', verbose_name=b'Allow guests to add music to the playlist (Recommended) ')),
                ('start_time', models.DateTimeField()),
                ('fb_event_id', models.TextField(default=None, max_length=256, blank=True)),
                ('fb_url', models.URLField()),
                ('slug', models.SlugField(editable=False)),
                ('djs', models.ManyToManyField(to='dj.DJ', blank=True)),
            ],
            options={
                'ordering': ['-created'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Venue', max_length=256, blank=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_positive', models.BooleanField(default=True)),
                ('event', models.ForeignKey(to='event.Event')),
                ('track', models.ForeignKey(to='music.Track')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(help_text=b'Where is the event?', to='event.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='tracks',
            field=models.ManyToManyField(to='music.Track', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
