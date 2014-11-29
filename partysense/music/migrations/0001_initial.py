# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IDType'
        db.create_table(u'music_idtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'music', ['IDType'])

        # Adding model 'ExternalID'
        db.create_table(u'music_externalid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('id_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.IDType'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'music', ['ExternalID'])

        # Adding model 'Artist'
        db.create_table(u'music_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'music', ['Artist'])

        # Adding M2M table for field _external_ids on 'Artist'
        m2m_table_name = db.shorten_name(u'music_artist__external_ids')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm[u'music.artist'], null=False)),
            ('externalid', models.ForeignKey(orm[u'music.externalid'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artist_id', 'externalid_id'])

        # Adding model 'Track'
        db.create_table(u'music_track', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['music.Artist'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'music', ['Track'])

        # Adding M2M table for field _external_ids on 'Track'
        m2m_table_name = db.shorten_name(u'music_track__external_ids')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('track', models.ForeignKey(orm[u'music.track'], null=False)),
            ('externalid', models.ForeignKey(orm[u'music.externalid'], null=False))
        ))
        db.create_unique(m2m_table_name, ['track_id', 'externalid_id'])


    def backwards(self, orm):
        # Deleting model 'IDType'
        db.delete_table(u'music_idtype')

        # Deleting model 'ExternalID'
        db.delete_table(u'music_externalid')

        # Deleting model 'Artist'
        db.delete_table(u'music_artist')

        # Removing M2M table for field _external_ids on 'Artist'
        db.delete_table(db.shorten_name(u'music_artist__external_ids'))

        # Deleting model 'Track'
        db.delete_table(u'music_track')

        # Removing M2M table for field _external_ids on 'Track'
        db.delete_table(db.shorten_name(u'music_track__external_ids'))


    models = {
        u'music.artist': {
            'Meta': {'object_name': 'Artist'},
            '_external_ids': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['music.ExternalID']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'music.externalid': {
            'Meta': {'object_name': 'ExternalID'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.IDType']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'music.idtype': {
            'Meta': {'object_name': 'IDType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'music.track': {
            'Meta': {'object_name': 'Track'},
            '_external_ids': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['music.ExternalID']", 'symmetrical': 'False'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['music.Artist']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['music']