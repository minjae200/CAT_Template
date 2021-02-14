from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from CCC.models import Job, Module
from CCC.forms import ModuleForm, JobForm
from CCC.Helper.ViewHelper import *
from CCC.Helper.DateHelper import *

# Create your views here.
def MainView(request):
    if request.method == 'GET':
        latest_job_list = Job.objects.all().order_by('-build_start_time')[:15]
        form = JobForm(request.GET)
        context = {
            'latest_job_list': latest_job_list,
            'username': "minjae.choi",
            'form': form
        }
        return render(request, 'main.html', context)
    else:
        form = JobForm(request.POST)
        return HttpResponseRedirect(reverse('CCC:create'))


def DetailView(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    try:
        if request.method == 'POST':
            form = ModuleForm(request.POST)
            if form.is_valid():
                if not is_valid_module(form.cleaned_data):
                    pass
                elif is_exist_module(job, form.cleaned_data):
                    messages.info(request, 'Already exist the module')
                else:
                    module_name = form.cleaned_data['name']
                    module_tag = form.cleaned_data['tag']
                    module_hash = form.cleaned_data['hash_value']
                    new_module = Module.objects.create(job=job, name=module_name, tag=module_tag, hash_value=module_hash)
                    new_module.save()
                form = ModuleForm()
        else:
            form = ModuleForm(request.GET)
        return render(request, 'detail.html', {'job': job, 'form': form})
    except (KeyError, Job.DoesNotExist):
        return render(request, 'main.html')

def AbortView(request, job_id):
    print("ABORT!!!")
    try:
        Job.objects.filter(pk=job_id).delete()
    except:
        pass
    return HttpResponseRedirect(reverse('CCC:main'))

def ForceStartView(request, job_id):
    print("START!!")
    return HttpResponseRedirect(reverse('CCC:main'))

def CreateJobView(request):
    print("CREATE JOB!")
    if request.method == 'POST':
        print("request post!")
        form = JobForm(request.POST)
        if form.is_valid() and form.cleaned_data['branch'] != '':
            build_time = get_time(request.POST.get('build_date'), request.POST.get('build_time'))
            Job.objects.create(branch=form.cleaned_data['branch'], build_start_time=build_time)
        form = JobForm()
    else:
        print("request get!")
        form = JobForm(request.GET)
    return HttpResponseRedirect(reverse('CCC:main'))