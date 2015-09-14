# -*- coding: UTF-8 -*-
from django import forms
import re

class NewMailForm(forms.Form):
    reader = forms.CharField(label=u'收件人', required=True)
    title = forms.CharField(label=u'标题', required=True)
    content = forms.CharField(label=u'内容', widget=forms.Textarea,required=True)
    
    def clean_reader(self):
        reader = self.cleaned_data['reader']
        url_number_list = re.findall('(\d+)',reader)
        return url_number_list
    
class NewAskForm(forms.Form):
    content = forms.CharField(label=u'内容', widget=forms.Textarea,required=True)