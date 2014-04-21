#!/usr/bin/python -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext

class SignUpForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    username = forms.CharField()
    password = forms.CharField()
    password_comfirmation = forms.CharField()
