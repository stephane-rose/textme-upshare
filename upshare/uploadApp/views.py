# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from registration.forms import RegistrationForm
from django import forms            

from uploadApp.models import User, File

# Create your views here.

def index(request):
    list_user = User.objects.all()
    context = {'list_user': list_user}
    return render(request, 'uploadApp/index.html', context)

def signup(request):
    return render(request, 'uploadApp/signUp.html')

def signin(request):
    return render(request, 'uploadApp/signIn.html')
def loggedin(request, username):
    return render(request, 'uploadApp/user.html')
