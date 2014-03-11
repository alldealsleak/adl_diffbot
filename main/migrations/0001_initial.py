# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(u'main_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Company'])

        # Adding model 'CurrentUrl'
        db.create_table(u'main_currenturl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Company'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['CurrentUrl'])

        # Adding model 'Media'
        db.create_table(u'main_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
        ))
        db.send_create_signal(u'main', ['Media'])

        # Adding model 'ProductSingapore'
        db.create_table(u'main_productsingapore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('offer_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('regular_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('merchant', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Media'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Company'])),
        ))
        db.send_create_signal(u'main', ['ProductSingapore'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table(u'main_company')

        # Deleting model 'CurrentUrl'
        db.delete_table(u'main_currenturl')

        # Deleting model 'Media'
        db.delete_table(u'main_media')

        # Deleting model 'ProductSingapore'
        db.delete_table(u'main_productsingapore')


    models = {
        u'main.company': {
            'Meta': {'object_name': 'Company'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'main.currenturl': {
            'Meta': {'object_name': 'CurrentUrl'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Company']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'main.media': {
            'Meta': {'object_name': 'Media'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        u'main.productsingapore': {
            'Meta': {'object_name': 'ProductSingapore'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Media']", 'null': 'True', 'blank': 'True'}),
            'merchant': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'offer_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'regular_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['main']