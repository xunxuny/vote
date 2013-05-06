#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.csrf.middleware import csrf_exempt
from django.template import Context, Template
from forms import SurveyForm
from models import  Survey,Option
from django.utils import simplejson
from datetime import datetime
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


model_class = Survey
base_template_name = "survey/"

def list(request):
    template_name = base_template_name + 'list.html'
    ctx={}
    objs=model_class.objects.all()
    ctx['objs']=objs
    ctx['menu_tree_selected_node'] = 'mt_ta_list'
    return render(request, template_name, ctx)

def new(request):
    form_class = SurveyForm
    template_name = base_template_name + 'new.html'
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return HttpResponseRedirect(reverse("table_detail", args=[obj.pk]))
    else:
        form = SurveyForm()
    ctx = { "form": form}
    ctx['menu_tree_selected_node'] = 'mt_ta_list'
    return render(request, template_name, ctx)

def detail(request,id):
    template_name = base_template_name + 'detail.html'
    obj=get_object_or_404(model_class,id=id)
    options=obj.option_set.all()
    ctx={'obj':obj,'options':options}
    return render(request, template_name, ctx)

def edit(request, id):
    """ 编辑投票项的基础信息 """
    obj = get_object_or_404(model_class, id=id)
    form = SurveyForm(instance=obj)
    if request.method == "POST":
        data=request.POST
        form = SurveyForm(data,instance=obj)
        if form.is_valid():
            o = form.save()
            return HttpResponseRedirect(reverse("table_detail", args=[obj.pk]))
    return  HttpResponse(Template("{{ form }}").render(Context({'form': form})))

def append(request, id):
    """ 添加投票选项信息 """
    obj = get_object_or_404(model_class, id=id)
    if request.method == "POST":
        name= request.POST.get('option_name','')
        if name:
            option=Option(subject=obj,name=name)
            option.save()
    return  HttpResponseRedirect(reverse("table_detail", args=[obj.pk]))

def launch(request, id):
    """ 发起投票 """
    obj = get_object_or_404(model_class, id=id)
    obj.status=u'started'
    obj.save()
    return  HttpResponseRedirect(reverse("table_detail", args=[obj.id]))

def finish(request, id):
    """ 关闭投票 """
    obj = get_object_or_404(model_class, id=id)
    obj.status=u'finished'
    obj.save()
    return  HttpResponseRedirect(reverse("table_list"))

def reset(request,id):
    """重置投票项"""
    obj = get_object_or_404(model_class, id=id)
    obj.status=u'unstarted'
    obj.save()
    for o in obj.option_set.all():
        o.voters.clear()
        o.votecount=0
        o.save()
    return  HttpResponseRedirect(reverse("table_list"))

def vote(request,id):
    """ 投票 """
    template_name = base_template_name + 'vote.html'
    users=[]
    is_vote=False
    obj=get_object_or_404(model_class,id=id)
    options=obj.option_set.all()
    for o in options:
        users.extend(o.voters.all())
    if request.user.is_anonymous() or request.user in users:
        is_vote=True
    if obj.status !=u'started':
        is_vote=True
    ctx={'obj':obj,'options':options,'is_vote':is_vote}
    return render(request, template_name, ctx)

def delete(request, id):
    """ 删除投票项 """
    obj = get_object_or_404(model_class, id=id)
    obj.delete()
    return HttpResponseRedirect(reverse("table_list"))

@csrf_exempt
def option_delete(request, id):
    """ 删除投票选项信息 """
    if request.method == "POST":
        option_ids = request.POST.get('options','').split(',')
        for option_id in option_ids:
            if option_id:
                option=get_object_or_404(Option,id=option_id)
                option.delete()
    return  HttpResponseRedirect(reverse("table_detail", args=[id]))

@csrf_exempt
def vote_load(request, id):
    """ 删除投票选项信息 """
    template_name = base_template_name + 'vote_form.html'
    users=[]
    is_vote=False
    voted=False
    obj=get_object_or_404(model_class,id=id)
    options=obj.option_set.all()
    for o in options:
        users.extend(o.voters.all())
    if request.user in users:
        is_vote=True
        voted=True
    if request.user.is_anonymous():
        is_vote=True
    if obj.status !=u'started':
        is_vote=True
    ctx={'obj':obj,'options':options,'is_vote':is_vote,'user':request.user,'timediff':(obj.end_time-datetime.now())}
    data={}
    from django.template.loader import get_template
    data['html']=get_template(template_name).render(Context(ctx))
    data['voted']=voted
    data['is_vote']=is_vote
    callback = request.GET['callback']

    return HttpResponse('%s(%s)' % (callback,
                simplejson.dumps(data)), mimetype='text/html')#application/json

@csrf_exempt
def vote_update(request, id):
    """ 删除投票选项信息 """
    option_ids = request.GET.get('options','').split(',')
    for option_id in option_ids:
        if option_id:
            option=get_object_or_404(Option,id=option_id)
            option.voters.add(request.user)
            option.save()
            option.votecount=option.voters.count()
            option.save()
    callback = request.GET['callback']
    return HttpResponse('%s(%s)'%(callback,simplejson.dumps({})), mimetype='text/html')


#load vote  #生成投票的html
#view vote
#vote #投票
