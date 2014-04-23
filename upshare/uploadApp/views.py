# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django import forms            
from uploadApp.models import MyUser, MyFile
from forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout as Logout
from django.http import HttpResponseRedirect
from django.conf import settings

from django import forms
import boto.s3
from boto.s3.key import Key

# Login / logout / subscribe

def index(request):
    if request.user.is_authenticated():
        list_files = request.user.myfile_set.all()
        return render(request, 'uploadApp/user.html', {'list_files' : list_files})
    return render(request, 'uploadApp/index.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'uploadApp/signUp.html')
    elif request.method == 'POST':
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
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        bad_login = True
        return render(request, 'uploadApp/index.html', {'bad_login' : bad_login})

def logout(request):
    Logout(request)
    return HttpResponseRedirect('/')

# upload / boto / Aws

def upload_boto(request):
    list_files = request.user.myfile_set.all()
    if request.method == 'POST':
        conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        
        bucket = conn.get_bucket('textme-srose')
        def percent_cb(complete, total):
            print complete
        epur_file_name = request.FILES['file'].name.replace(' ', '_')
        media_key = "media/" + request.user.username + "/" + epur_file_name
        if not bucket.get_key(media_key):
            k = bucket.new_key("media/" + request.user.username + "/" + epur_file_name)
            k.set_metadata('Content-Type', request.FILES['file'].content_type)
            k.set_metadata('Cache-Control', 'max-age=864000')
            if (k.set_contents_from_string(request.FILES['file'].read(), cb=percent_cb, num_cb=10) != 0 and request.POST.get('time_available') > 0):
                url = k.generate_url(int(request.POST.get('time_available')) * 86400, method='GET')
                k.make_public()
                urlTmp = "https://textme-srose.s3.amazonaws.com/media/" + request.user.username + "/" + request.FILES['file'].name
                urlTmp = urlTmp.replace(' ', '_')
                print urlTmp
                newFile = MyFile.objects.create(file_name=epur_file_name, 
                                                user = request.user, shortlink = urlTmp)
                newFile.save()
                return render(request, 'uploadApp/uploadsuccess.html')
    return render(request, 'uploadApp/user.html', {'list_files' : list_files})


def success(request):
    return HttpResponse("YIPEEEEE")
