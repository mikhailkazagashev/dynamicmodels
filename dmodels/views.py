from django.http import HttpResponse
from django.shortcuts import render, redirect
from dmodels.forms import UploadFileForm
from yamodel import model_from_yaml
import yaml
from django.contrib import admin
from django.views.generic import ListView
from django.forms import ModelForm

def create(request):
    cont={}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                models = yaml.load(request.FILES['file'].read())
                for m in models:
                    model_from_yaml(m)
                return redirect('/models_list')
            except Exception as e:
                cont['error']='There was an error creating models from this file  '+str(e)
    cont['form']=UploadFileForm()
    return render(request,'create.html', cont)

def show(request,name):
    for mdl in admin.site._registry:
        if mdl.__name__==name: break
    else:
        return redirect('/admin')

    class DForm(ModelForm):
        class Meta:
            model = mdl
            exclude = ['id']
            
    form = DForm()
    objects = mdl.objects.all().values()    
    fields=mdl._meta.fields
    return render(request,'show.html', { 'objects':objects, 'fields':fields,'form':form,'name':name})
    
    
def models_list(request):
    models=[]
    for model in admin.site._registry:
        if model._meta.app_label=='dmodels':
            models.append({'name':model.__name__,'verbose_name':model.verbose_name})
    return render(request,'models_list.html', {'models':models})
    
    
