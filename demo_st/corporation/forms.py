# -*- coding: UTF-8 -*-
from django import forms

class CreatCorporationForm(forms.Form):
    name = forms.CharField()
    introduction = forms.CharField()
    birthyear = forms.IntegerField()
    school = forms.CharField()
    
class CreatDepartmentForm(forms.Form):
    department_name = forms.CharField(required=False)


class DeleteDepartmentForm(forms.Form):
    department_name = forms.CharField(required=False)
    
class MoveMemberForm(forms.Form):
    department_name = forms.CharField(required=False)
    user_url_number = forms.IntegerField()
    
    
class ModifyCorporationForm(forms.Form):
    name = forms.CharField(required=False)
    introduction = forms.CharField()