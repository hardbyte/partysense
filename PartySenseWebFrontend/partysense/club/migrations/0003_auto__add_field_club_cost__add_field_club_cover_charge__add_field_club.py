# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Club.cost'
        db.add_column(u'club_club', 'cost',
                      self.gf('django.db.models.fields.CharField')(default='med', max_length=3, blank=True),
                      keep_default=False)

        # Adding field 'Club.cover_charge'
        db.add_column(u'club_club', 'cover_charge',
                      self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Club.live_music'
        db.add_column(u'club_club', 'live_music',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Club.dress_code'
        db.add_column(u'club_club', 'dress_code',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1, blank=True),
                      keep_default=False)

        # Adding field 'Club.style'
        db.add_column(u'club_club', 'style',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'Club.uses_partysense'
        db.add_column(u'club_club', 'uses_partysense',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Club.live_on_partysense'
        db.add_column(u'club_club', 'live_on_partysense',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field djs on 'Club'
        m2m_table_name = db.shorten_name(u'club_club_djs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('club', models.ForeignKey(orm[u'club.club'], null=False)),
            ('dj', models.ForeignKey(orm[u'dj.dj'], null=False))
        ))
        db.create_unique(m2m_table_name, ['club_id', 'dj_id'])


        # Changing field 'Club.website'
        db.alter_column(u'club_club', 'website', self.gf('django.db.models.fields.URLField')(max_length=256))

        # Changing field 'Club.facebook_page'
        db.alter_column(u'club_club', 'facebook_page', self.gf('django.db.models.fields.URLField')(max_length=256))

    def backwards(self, orm):
        # Deleting field 'Club.cost'
        db.delete_column(u'club_club', 'cost')

        # Deleting field 'Club.cover_charge'
        db.delete_column(u'club_club', 'cover_charge')

        # Deleting field 'Club.live_music'
        db.delete_column(u'club_club', 'live_music')

        # Deleting field 'Club.dress_code'
        db.delete_column(u'club_club', 'dress_code')

        # Deleting field 'Club.style'
        db.delete_column(u'club_club', 'style')

        # Deleting field 'Club.uses_partysense'
        db.delete_column(u'club_club', 'uses_partysense')

        # Deleting field 'Club.live_on_partysense'
        db.delete_column(u'club_club', 'live_on_partysense')

        # Removing M2M table for field djs on 'Club'
        db.delete_table(db.shorten_name(u'club_club_djs'))


        # Changing field 'Club.website'
        db.alter_column(u'club_club', 'website', self.gf('django.db.models.fields.URLField')(max_length=70))

        # Changing field 'Club.facebook_page'
        db.alter_column(u'club_club', 'facebook_page', self.gf('django.db.models.fields.URLField')(max_length=70))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'club.club': {
            'Meta': {'object_name': 'Club'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'cost': ('django.db.models.fields.CharField', [], {'default': "'med'", 'max_length': '3', 'blank': 'True'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'cover_charge': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'djs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dj.DJ']", 'symmetrical': 'False'}),
            'dress_code': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'facebook_page': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['music.Genre']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_music': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'live_on_partysense': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'style': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'uses_partysense': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dj.dj': {
            'Meta': {'object_name': 'DJ'},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'event.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'music.genre': {
            'Meta': {'object_name': 'Genre'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        }
    }

    complete_apps = ['club']