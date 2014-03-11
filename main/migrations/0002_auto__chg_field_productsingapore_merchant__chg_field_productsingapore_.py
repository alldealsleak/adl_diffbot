# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ProductSingapore.merchant'
        db.alter_column(u'main_productsingapore', 'merchant', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'ProductSingapore.title'
        db.alter_column(u'main_productsingapore', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'ProductSingapore.product_id'
        db.alter_column(u'main_productsingapore', 'product_id', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Media.caption'
        db.alter_column(u'main_media', 'caption', self.gf('django.db.models.fields.CharField')(max_length=500))

    def backwards(self, orm):

        # Changing field 'ProductSingapore.merchant'
        db.alter_column(u'main_productsingapore', 'merchant', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'ProductSingapore.title'
        db.alter_column(u'main_productsingapore', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'ProductSingapore.product_id'
        db.alter_column(u'main_productsingapore', 'product_id', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Media.caption'
        db.alter_column(u'main_media', 'caption', self.gf('django.db.models.fields.CharField')(max_length=50))

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
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
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
            'merchant': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'offer_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'product_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'regular_price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['main']