#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

import  views

urlpatterns = patterns('',
    #Packing
    url(r'^$', views.list, name='table_list'),
    url(r'^new/$', views.new, name='table_new'),
    url(r'^(?P<id>\d+)/$',views.detail,name='table_detail'),
    url(r'^(?P<id>\d+)/edit/$', views.edit, name='table_edit'),
    url(r'^(?P<id>\d+)/append/$', views.append, name='table_append'),
    url(r'^(?P<id>\d+)/vote/$', views.vote, name='table_vote'),
    url(r'^(?P<id>\d+)/launch/$', views.launch, name='table_launch'),
    url(r'^(?P<id>\d+)/finish/$', views.finish, name='table_finish'),
    url(r'^(?P<id>\d+)/reset/$', views.reset, name='table_reset'),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name='table_delete'),
    url(r'^(?P<id>\d+)/option_delete/$', views.option_delete, name='option_delete'),
    url(r'^(?P<id>\d+)/vote_load/$', views.vote_load, name='vote_form_load'),
    url(r'^(?P<id>\d+)/vote_update/$', views.vote_update, name='vote_form_update'),
)

urlpatterns += patterns('',

)
