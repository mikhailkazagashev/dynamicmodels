# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from models import Modelsname
from django.core.urlresolvers import clear_url_caches
from django.utils.importlib import import_module
from django.conf import settings
from django.views.generic import ListView

def create_model(name, fields=None, app_label='', module=''):
    """
    Create specified model
    """
    class Meta:
        pass

    if app_label:
        setattr(Meta, 'app_label', app_label)

    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)
        
    model = type(name, (models.Model,), attrs)

    admin.site.register(model)
    reload(import_module(settings.ROOT_URLCONF))
    clear_url_caches()    
    return model

def install(model):
    from django.core.management import sql, color
    from django.db import connection

    style = color.no_style()

    cursor = connection.cursor()
    statements, pending = connection.creation.sql_create_model(model, style, [])
    for sql in statements:
        cursor.execute(sql)

def getfield(field_type,title):
    if field_type=='char':
        return models.CharField(title,max_length=255)
    if field_type=='int':
        return models.IntegerField(title)
    if field_type=='date':
        return models.DateField(title)

def model_from_yaml(d):
    '''
    if d['name']=='dmodels':
        raise Exception("Incorrect model's name")
    '''
    fields = {}
    for fld in d['fields']:
        fields[fld['id']] = getfield(fld['type'],fld['title'])
    fields['verbose_name'] = d['title']
    model = create_model(d['name'],fields,app_label='dmodels',module='dmodels.models')
    install(model)
    Modelsname(name=d['name']).save()
        

def remove_tables():
    from django.db import connection
    cursor = connection.cursor()
    for m in Modelsname.objects.all():
        cursor.execute('DROP TABLE IF EXISTS dmodels_%s' % m.name)
    Modelsname.objects.all().delete()
