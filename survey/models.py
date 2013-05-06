#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User

class Survey(models.Model):
    SURVEY_STATUS_CHOICES =(
        (u'unstarted', u'未发起'),
        (u'started', u'发起'),
        (u'finished', u'完成'),
        )
    SURVEY_TYPE_CHOICE =(
        (u'radio', u'单选'),
        (u'checkbox', u'多选'),
        )
    name = models.CharField(u'名称', max_length=255, blank=True,
            help_text=u'投票的名称')
    descn = models.TextField(u'描述', blank=True,max_length=255,
            help_text=u'投票的描述')
    type = models.CharField(u'类型',max_length=255, default='single',choices = SURVEY_TYPE_CHOICE)
    status = models.CharField(u'状态', max_length=255,default='unstarted',choices = SURVEY_STATUS_CHOICES)
    end_time = models.DateTimeField(null=True, blank=True,help_text=u'格式为2012-01-09 12:30:00 或 2012-1-9 14:30')#关闭时间

    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True, blank = True, null = True)
    created_by = models.ForeignKey(User)
        
    def __unicode__(self):
        return self.name

    def vote_total(self):
        total = 0.0
        for o in self.option_set.all():
            total += o.votecount
        return total

class Option(models.Model):
    subject = models.ForeignKey(Survey)
    name = models.CharField(u'名称', max_length=255, blank=True,
            help_text=u'选项的名称')
    votecount = models.FloatField(u'票选数', default=0,help_text=u'')
    voters = models.ManyToManyField(User,null=True,blank=True)


    def __unicode__(self):
        return u'%s--%s'%(self.subject.name,self.name)

    def count_percentage(self):
        per=0.0
        if self.subject.vote_total()!=0.0:
            per = self.votecount*100/self.subject.vote_total()
        return  u'%s%%'% int(per)

    def show_voters(self):
        voters= [u.username for u in self.voters.all()]
        return ', '.join(voters)
