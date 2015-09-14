# -*- coding: UTF-8 -*-
from django import forms

class NewReplyForm(forms.Form):
    content = forms.CharField(label=u'回应', widget=forms.Textarea,required=True)
