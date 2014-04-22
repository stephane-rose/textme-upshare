# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MyUser(User):
    def __unicode__(self):
        return self.get_full_name()

class MyFile(models.Model):
    file_name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    shortlink = models.CharField(max_length=200)
    def __unicode(self):
        return self.shortlink
