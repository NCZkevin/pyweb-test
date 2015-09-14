# -*- coding: UTF-8 -*-
from django import forms
from accounts.models import Student
from django.forms.util import ErrorList

class AccountsErrorList(ErrorList):
    def __unicode__(self):
        return self.as_bootstrap()
    def as_bootstrap(self):
        if not self:
            return u''
        else:
            return u'<p class="alert alert-error">%s</p>' % '<br />'.join(self)

class AccountsSignupForm(forms.Form):
    error_messages = {
        'duplicate_email': u'此邮箱已经注册',
    }
    email = forms.EmailField(error_messages={'required': u'请输入电子邮件地址', 'invalid': u'请输入有效的电子邮件地址'})
    password = forms.CharField()
    realname = forms.CharField()
    gender = forms.CharField()



    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Student.objects.get(email=email)
        except Student.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
    
        
     
class AccountsLoginForm(forms.Form):
    login_email = forms.EmailField(max_length=128, label=u'电子邮件')
    login_password = forms.CharField(min_length=6,label=u'密码')
    remember_me = forms.CharField(required=False)
    
    
    

class AccountsModifyProfileForm(forms.Form):
    realname = forms.CharField(label=u'真实姓名',max_length=5,min_length=1)
    face = forms.ImageField(label=u'头像', required=False)
    school = forms.CharField(label=u'学校', required=False)
    birthday = forms.DateField(label=u'生日')
    
    
    
    
class NewFeedForm(forms.Form):
    content = forms.CharField(required=False,widget=forms.Textarea)
    

     
class AccountsModifyPasswordForm(forms.Form):       
    pass

