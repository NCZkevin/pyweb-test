# -*- coding: UTF-8 -*-
from django import forms

class CreatActivityForm(forms.Form):
    name = forms.CharField(required=True, label=u'活动名称')
    start_time = forms.DateTimeField(required=True, label=u'开始时间')
    finish_time = forms.DateTimeField(required=True, label=u'结束时间')
    place = forms.CharField(required=True, label=u'活动地点')
    max_student = forms.IntegerField(label=u'人数上限')
    pay = forms.IntegerField(label=u'人均消费')
    detail = forms.CharField(required=False,widget=forms.Textarea, label=u'补充细节')