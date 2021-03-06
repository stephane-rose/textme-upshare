from django.conf.urls import patterns, url, include
from uploadApp import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^signup/$', views.signup, name='signup'),
                       url(r'^signin/$', views.signin, name='signin'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^do_upload/$', views.upload_boto, name='do_upload'),
                       url(r'^success/$', views.success, name='success'),
)
