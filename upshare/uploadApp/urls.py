from django.conf.urls import patterns, url, include
from uploadApp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^signup/$', views.signup, name='signup'),
                       url(r'^signin/$', views.signup, name='signin'),
                       url(r'^(?P<username>\D+)/user/$', views.loggedin, name='loggedin'),
)
