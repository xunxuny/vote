#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.contrib import admin

from models import Survey,Option


class SurveyAdmin(admin.ModelAdmin):    
    list_display = ('name', 'type', 'status', 'created_by', )
    search_fields = ('name', 'created_by__username')

class OptionAdmin(admin.ModelAdmin):    
    list_display = ('name', 'subject', 'votecount', 'show_voters', )
    search_fields = ('name', 'subject__name')

admin.site.register(Survey,SurveyAdmin)
admin.site.register(Option,OptionAdmin)
