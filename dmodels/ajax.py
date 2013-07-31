from django.template.loader import render_to_string
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib import admin
from django.template import RequestContext
from django.forms import ModelForm
from dajaxice.utils import deserialize_form
from django.shortcuts import render, redirect
from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import extras

def get_model(name):
    for model in admin.site._registry:
        if model.__name__==name: break
    else:
        return False
    return model

def get_form(mdl,form=False):
    class DForm(ModelForm):
        class Meta:
            model = mdl

        def __init__(self, *args, **kwargs):
            super(ModelForm, self).__init__(*args, **kwargs)
            for f in mdl._meta.fields:
                if type(f)==models.DateField:
                    self.fields[f.name].widget=extras.widgets.SelectDateWidget()
                    #self.fields[f.name].widget=AdminDateWidget() 
    if form:
        return DForm(form)
    else:
        return DForm()
    
@dajaxice_register
def get_data(request, name):
    model=get_model(name)
    if not model:
        return redirect('/create')
            
    form =  get_form(model)
    
    objects = model.objects.all().values()    
    fields=model._meta.fields
    html=render_to_string('show.html',
                           { 'objects':objects, 'fields':fields,'form':form,'name':name},
                           context_instance = RequestContext(request))

    dajax = Dajax()
    dajax.assign('#model_info', 'innerHTML', html)
    return dajax.json()

@dajaxice_register
def add_data(request, form, name):
    model=get_model(name)
    if not model:
        return redirect('/create')
            
    form = get_form(model,deserialize_form(form))

    dajax = Dajax()
    if form.is_valid():
        new = form.save()
        objects = model.objects.all().values()    
        fields=model._meta.fields
        html=render_to_string('show_data.html',
                               { 'objects':objects, 'fields':fields,'form':form,'name':name},
                               context_instance = RequestContext(request))

        dajax.assign('#data', 'innerHTML', html)
        dajax.assign('#data_errors', 'innerHTML', '')
    else:
        dajax.assign('#data_errors', 'innerHTML', 'Correct the following fields: %s' % form.errors)

    return dajax.json()

