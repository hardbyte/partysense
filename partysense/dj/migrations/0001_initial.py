# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DJ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=70, verbose_name=b'Alias')),
                ('email', models.EmailField(max_length=254)),
                ('url', models.URLField(verbose_name=b'Facebook Page or website', blank=True)),
                ('city_name', models.CharField(help_text=b'What city are you based in?', max_length=70, verbose_name=b'Location')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
