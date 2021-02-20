from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from CCC.models import Job, Module
from CCC.forms import ModuleForm, JobForm
from CCC.Helper.ViewHelper import *
from CCC.Helper.DateHelper import *
from CCC.Helper.ThreadHelper import ThreadPool

# Create your views here.
def MainView(request):
    latest_job_list = Job.objects.all().order_by('-build_start_time')
    paginator = Paginator(latest_job_list, 10)
    page = request.GET.get('page')
    latest_job_list = paginator.get_page(page)
    form = JobForm(request.GET)
    context = {
        'latest_job_list': latest_job_list,
        'username': "minjae.choi",
        'form': form
    }
    return render(request, 'main.html', context)

def DetailModalView(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    context = {
        'job': job
    }
    return render(request, 'detail.html', context)

def DetailView(request, job_id):
    try:
        job = get_object_or_404(Job, pk=job_id)
        if request.method=='POST':
            module_name = request.POST['module_name']
            module_tag = request.POST['module_tag']
            module_hash = request.POST['module_hash']
            module = {
                'name': module_name,
                'tag': module_tag,
                'hash_value': module_hash
            }
            if not is_valid_module(module):
                # messages.warning(request, 'Please input the module')
                module['messages'] = {
                    'type': 'warning',
                    'content': 'Please input the module'
                }
            elif is_exist_module(job, module):
                # messages.warning(request, 'Already exist the module')
                module['messages'] = {
                    'type': 'warning',
                    'content': 'Already exist the module'
                }
            else:
                new_module = Module.objects.create(job=job, name=module_name, tag=module_tag, hash_value=module_hash)
                new_module.save()
                # messages.success(request, 'Register Success')
                module['messages'] = {
                    'type': 'success',
                    'content': 'Register Success'
                }
        else:
            module = {}
    except:
        pass
    return JsonResponse(module)

@csrf_exempt
def DeleteModuleView(request, job_id, module_id):
    result = {'messages': {'type': '', 'content': ''}}
    try:
        job = get_object_or_404(Job, pk=job_id)
        if request.method == 'POST':
            module = job.module_set.all().filter(pk=module_id)
            module_name = module[0].name
            module.delete()
            result['messages'] = {
                'type': 'success',
                'content': 'Delete Success! ({})'.format(module_name)
            }
        else:
            pass
    except Exception as Error:
        result['messages'] = {
            'type': 'warning',
            'content': '{}'.format(Error)
        }
    finally:
        return JsonResponse(result)

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
            # Thread(1) - Scheduler -> Build Start -> Observer create
            
        form = JobForm()
    else:
        print("request get!")
        form = JobForm(request.GET)
    return HttpResponseRedirect(reverse('CCC:main'))