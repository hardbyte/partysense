# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Genre'
        db.create_table(u'music_genre', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'music', ['Genre'])


    def backwards(self, orm):
        # Deleting model 'Genre'
        db.delete_table(u'music_genre')


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
        u'music.genre': {
            'Meta': {'object_name': 'Genre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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