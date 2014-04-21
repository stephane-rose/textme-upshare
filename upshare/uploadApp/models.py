# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(User):
    def __unicode__(self):
        return self.get_full_name()
class File(models.Model):
    file_name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    url = models.URLField(max_length=200)
    shortlink = models.CharField(max_length=70)
    expiry_date = models.DateTimeField()

    def __unicode(self):
        return self.url
