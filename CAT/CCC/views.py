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
    latest_job_list = Job.objects.all().order_by('build_start_time')[:10]
    context = {'latest_job_list': latest_job_list}
    return render(request, 'main.html', context)

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
    except (KeyError, Module.DoesNotExist):
        return render(request, 'main.html')

def AbortView(request, job_id):
    print("ABORT!!!")
    # return HttpResponseRedirect(reverse('CCC:detail', args=(job_id,)))
    return HttpResponseRedirect(reverse('CCC:main'))

def ForceStartView(request, job_id):
    print("START!!")
    return HttpResponseRedirect(reverse('CCC:main'))

def CreateView(request):
    param = {}
    if request.method == 'POST':
        form = JobForm(request.POST)
        if not form.is_valid() or form.cleaned_data['branch'] == '':
            return HttpResponseRedirect(reverse('CCC:create'))
        build_time = get_time(request.POST.get('build_date'), request.POST.get('build_time'))
        if build_time is None:
            build_time = default_start_time()
        new_job = Job.objects.create(branch=form.cleaned_data['branch'], build_start_time=build_time)
        form = JobForm()
    else:
        form = JobForm(request.GET)
    return render(request, 'create.html', {'form': form})

def CreateJobView(request):
    print("CREATE JOB!")
    return HttpResponseRedirect(reverse('CCC:main'))
