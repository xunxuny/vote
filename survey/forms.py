#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from models import Survey



class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ['name', 'type', 'descn','end_time']

    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)