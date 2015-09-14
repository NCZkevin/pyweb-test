# Create your views here.
from sitemail.models import Sitemail
from django.shortcuts import render_to_response
from demo_COC.settings import STATIC_URL
from django.template import RequestContext
from forms import NewMailForm
from relations.models import S_S_Card
from accounts.models import Student
import datetime
from django.http import HttpResponseRedirect
import re
from reply.forms import NewReplyForm
from reply.models import Reply


def inbox(request):
    inmail_list = Sitemail.objects(creator__in=request.user.get_sscard_as_target())
    return render_to_response('sitemail/inbox.html', {'inmail_list':inmail_list, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def outbox(request):
    outmail_list = Sitemail.objects(creator__in=request.user.get_sscard_as_user())
    return render_to_response('sitemail/outbox.html', {'outmail_list':outmail_list, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def showmail(request, url_number):
    mail = Sitemail.objects(url_number=url_number).get()
    if request.user in [a.target for a in mail.creator]:
        mail.is_readed = True
        mail.save()
        
    if request.method == "POST":
        form = NewReplyForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            reply = Reply(content=content)
            sscard = S_S_Card.objects.get_or_create(user=request.user, target=mail.creator[0].user)
            reply.creator = sscard[0]
            reply.creat_time = datetime.datetime.now()
            reply.target = mail
            reply.is_active = True
            reply.save()
            return HttpResponseRedirect('')
            
    else:
        return render_to_response('sitemail/showmail.html',{'mail':mail, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
    
def sendmail(request):
    if request.method == 'POST':
        form = NewMailForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            readers = form.cleaned_data['reader']
            targets = Student.objects(url_number__in=readers)
            creators = S_S_Card.objects(user=request.user, target__in=targets)
            print creators
            url_number = len(Sitemail.objects) + 1
            mail = Sitemail(title=title, content=content, creator=creators, creat_time=datetime.datetime.now(), is_readed=False, url_number=url_number).save()
            return HttpResponseRedirect('/sitemail/outbox/')
        
    else:
        form = NewMailForm()
        return render_to_response('sitemail/sendmail.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user, 'form':form}, context_instance=RequestContext(request))

        
        
        