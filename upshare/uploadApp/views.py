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

import boto.s3
import sys
from boto.s3.key import Key

# Login / logout / subscribe

def index(request):
    if request.user.is_authenticated():
        return render(request, 'uploadApp/user.html')
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
        print "ENVOIE BAD LOGIN"
        return render(request, 'uploadApp/index.html', {'bad_login' : "true"})

def logout(request):
    Logout(request)
    return HttpResponseRedirect('/')

# upload / boto / Aws

AWS_ACCESS_KEY_ID = 'AKIAI36GFMLSGYHNNLUA'
AWS_SECRET_ACCESS_KEY = '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'

def upload_boto(request):
    
    bucket_name = AWS_ACCESS_KEY_ID.lower() + '-textme-srose'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                           AWS_SECRET_ACCESS_KEY)
    
    bucket = conn.create_bucket(bucket_name,
                                location=boto.s3.connection.Location.DEFAULT)
    
    testfile = "replace this with an actual filename"
    print 'Uploading %s to Amazon S3 bucket %s' % \
        (testfile, bucket_name)
    
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
        
        k = Key(bucket)
        k.key = 'my test file'
        k.set_contents_from_filename(testfile,
                                     cb=percent_cb, num_cb=10)
        
