# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'main_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('depth', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['Category'])

        # Adding M2M table for field children on 'Category'
        m2m_table_name = db.shorten_name(u'main_category_children')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_category', models.ForeignKey(orm[u'main.category'], null=False)),
            ('to_category', models.ForeignKey(orm[u'main.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_category_id', 'to_category_id'])

        # Adding model 'ProductVietnam'
        db.create_table(u'main_productvietnam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Category'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('offer_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('regular_price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('merchant', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('media', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Media'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Company'])),
        ))
        db.send_create_signal(u'main', ['ProductVietnam'])

        # Adding field 'ProductSingapore.category'
        db.add_column(u'main_productsingapore', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Category'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'main_category')

        # Removing M2M table for field children on 'Category'
        db.delete_table(db.shorten_name(u'main_category_children'))

        # Deleting model 'ProductVietnam'
        db.delete_table(u'main_productvietnam')

        # Deleting field 'ProductSingapore.category'
        db.delete_column(u'main_productsingapore', 'category_id')


    models = {
        u'main.category': {
            'Meta': {'object_name': 'Category'},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'depth': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Category']", 'null': 'True', 'blank': 'True'}),
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
        },
        u'main.productvietnam': {
            'Meta': {'object_name': 'ProductVietnam'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Category']", 'null': 'True', 'blank': 'True'}),
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