from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, JsonResponse
from django.urls import reverse
from django.contrib import messages
from CAT.forms import LoginForm
from CCC.Helper.LoginHelper import authenticate, login_required

def LoginView(request):
    print("!!")
    if request.method == 'POST':
        try:
            form = LoginForm(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user_info = authenticate(username, password)
            if user_info:
                request.session['username'] = username
                request.session['password'] = password
                request.session['mail'] = user_info['mail']
                request.session['department'] = user_info['department']
                # sessionid = request.session.session_key
                return HttpResponseRedirect(reverse('CCC:main'))
            else:
                raise
        except Exception as error:
            print(error)
            messages.error(request,'username or password not correct')
            return redirect('login')
    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})

def RequiredView(request):
    return redirect('login')