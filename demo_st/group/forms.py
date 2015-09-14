# -*- coding: UTF-8 -*-
from django import forms

class CreatGroupForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()  # 小组简介
    # tags = fields.ListField(fields.StringField())#小组标签
    # school = fields.StringField()
    grouptype = forms.CharField()  # 小组类型，是否为私密小组
    
class ModifyGroupForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()