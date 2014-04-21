# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django import forms            

from uploadApp.models import User, File
from forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as Logout
from django.http import HttpResponseRedirect

def index(request):
    if request.user.is_authenticated():
        return render(request, 'uploadApp/user.html')
    return render(request, 'uploadApp/index.html')

def signup(request):
    print request.method
    if request.method == 'GET':
        return render(request, 'uploadApp/signUp.html')
    elif request.method == 'POST':
        print 'post!'
        print request.POST
        if request.POST.get('password') == request.POST.get('password_confirmation'):
            user = User.objects.create(first_name=request.POST.get('first_name'),
                                last_name=request.POST.get('last_name'),
                                email=request.POST.get('email'),
                                username=request.POST.get('username'))
            user.set_password(request.POST.get('password'))
            user.save()
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user:
                login(request, user)
            return render(request, 'uploadApp/user.html')

def signin(request):
    print request.POST
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse("failed")

def logout(request):
    Logout(request)
    return HttpResponseRedirect('/')
