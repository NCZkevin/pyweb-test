# -*- coding: UTF-8 -*-
import os
import datetime
from PIL import Image
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from demo_COC.settings import STATIC_URL, MEDIA_ROOT, MEDIA_URL
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from forms import CreatCorporationForm,ModifyCorporationForm,MoveMemberForm,CreatDepartmentForm,DeleteDepartmentForm
from models import Corporation
from reply.models import Reply
from reply.forms import NewReplyForm
from topic.models import Topic
from topic.forms import NewTopicForm, ModifyTopicForm
from activity.forms import CreatActivityForm
from activity.models import Activity
from relations.models import S_C_Card, S_S_Card
from django.template import RequestContext
from mongoengine.django.sessions import MongoSession
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from sitemail.forms import NewAskForm
from sitemail.models import Sitemail

def creat_corporation(request):
    if request.method == "POST":
        form = CreatCorporationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            birthyear = form.cleaned_data['birthyear']
            school = form.cleaned_data['school']
            corporation = Corporation(name=name, introduction=introduction, school=school, birthyear=birthyear, logo=STATIC_URL + 'img/face.png', thumbnail=STATIC_URL + 'img/face.png')
            url_number = len(Corporation.objects) + 1
            corporation.url_number = url_number
            corporation.creat_time = datetime.datetime.now()
            if request.FILES:
                path = 'img/corporation/' + str(url_number)
                if not os.path.exists(MEDIA_ROOT + path):
                    os.makedirs(MEDIA_ROOT + path)
                
                img = Image.open(request.FILES['logo'])
                if img.mode == 'RGB':
                    filename = 'logo.jpg'
                    filename_thumbnail = 'thumbnail.jpg'
                elif img.mode == 'P':
                    filename = 'logo.png'
                    filename_thumbnail = 'thumbnail.png'
                filepath = '%s/%s' % (path, filename)
                filepath_thumbnail = '%s/%s' % (path, filename_thumbnail)
                # 获得图像的宽度和高度
                width, height = img.size
                # 计算宽高
                ratio = 1.0 * height / width
                # 计算新的高度
                new_height = int(288 * ratio)
                new_size = (288, new_height)
                # 缩放图像
                if new_height >= 288:
                    thumbnail_size = (0,0,288,288)
                else:
                    thumbnail_size = (0,0,new_height,new_height)
                    
                out = img.resize(new_size, Image.ANTIALIAS)
                thumbnail = out.crop(thumbnail_size)
                thumbnail.save(MEDIA_ROOT + filepath_thumbnail)
                corporation.thumbnail = MEDIA_URL + filepath_thumbnail
                out.save(MEDIA_ROOT + filepath)
                corporation.logo = MEDIA_URL + filepath
                
            corporation.save()
            sccard = S_C_Card(user=request.user, corporation=corporation, is_active=True, is_admin=True,creat_time=datetime.datetime.now())
            sccard.save()
            return HttpResponseRedirect('/corporation/' + str(url_number) + '/')
        
        else:
            return HttpResponseNotFound("出错了。。。。。")
        
    else:
        form = CreatCorporationForm()
        return render_to_response('corporation/creat_corporation.html', {'form':form, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
                
                 

def showtopic(request, gurl_number, turl_number):
    corporation = Corporation.objects(url_number=gurl_number).get()
    topic = Topic.objects(url_number=turl_number).get()
    if request.method == 'POST':
        if "reply" in request.POST:
            reply_form = NewReplyForm(request.POST)
            if reply_form.is_valid():
                content = reply_form.cleaned_data['content']
                reply = Reply(content=content)
                sccard = S_C_Card.objects(user=request.user, corporation=corporation).get()
                reply.creator = sccard
                reply.creat_time = datetime.datetime.now()
                reply.target = topic
                reply.is_active = True
                reply.save()
                topic.update_author = request.user
                topic.update_time = datetime.datetime.now()
                topic.clicks = topic.clicks - 1
                topic.save()
                return HttpResponseRedirect('/corporation/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
            
        if "modify" in request.POST:
            modify_form = ModifyTopicForm(request.POST)
            if modify_form.is_valid():
                content = modify_form.cleaned_data['content']
                topic.content = content
                topic.clicks = topic.clicks - 1
                topic.save()
                return HttpResponseRedirect('/corporation/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
        
    else:
        reply_form = NewReplyForm()
        modify_form = ModifyTopicForm()
        topic.clicks = topic.clicks + 1
        topic.save()
        return render_to_response('corporation/topic_corporation.html', {'corporation':corporation, 'current_user':request.user, 'reply_form':reply_form, 'topic':topic, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

def showactivity(request, gurl_number, turl_number):
    corporation = Corporation.objects(url_number=gurl_number).get()
    activity = Activity.objects(url_number=turl_number).get()
    if request.method == 'POST':
        if "reply" in request.POST:
            reply_form = NewReplyForm(request.POST)
            if reply_form.is_valid():
                content = reply_form.cleaned_data['content']
                reply = Reply(content=content)
                sccard = S_C_Card.objects(user=request.user, corporation=corporation).get()
                reply.creator = sccard
                reply.creat_time = datetime.datetime.now()
                reply.target = activity
                reply.is_active = True
                reply.save()
                activity.clicks = topic.clicks - 1
                activity.save()
                return HttpResponseRedirect('/corporation/' + str(gurl_number) + '/activity/' + str(turl_number) + '/')
            
        
    else:
        reply_form = NewReplyForm()
        activity.clicks = activity.clicks + 1
        activity.save()
        return render_to_response('corporation/activity_corporation.html', {'corporation':corporation, 'current_user':request.user, 'reply_form':reply_form, 'activity':activity, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))


    
def my_corporations_creat(request):
    return render_to_response('corporation/my_corporations_creat.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def my_corporations_news(request):
    return render_to_response('corporation/my_corporations_news.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def my_corporations_reply(request):
    return render_to_response('corporation/my_corporations_reply.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def ask_for_admin(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    corporation.ask_for_admin(request.user)
    return HttpResponse('success')
                
                
def corporation_manage_edit(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    if request.method == "POST":
        form = ModifyCorporationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            corporation.update(set__name=name, set__introduction=introduction)
            if request.FILES:
                path = 'img/corporation/' + str(url_number)
                if not os.path.exists(MEDIA_ROOT + path):
                    os.makedirs(MEDIA_ROOT + path)
                
                img = Image.open(request.FILES['logo'])
                if img.mode == 'RGB':
                    filename = 'logo.jpg'
                    filename_thumbnail = 'thumbnail.jpg'
                elif img.mode == 'P':
                    filename = 'logo.png'
                    filename_thumbnail = 'thumbnail.png'
                filepath = '%s/%s' % (path, filename)
                filepath_thumbnail = '%s/%s' % (path, filename_thumbnail)
                # 获得图像的宽度和高度
                width, height = img.size
                # 计算宽高
                ratio = 1.0 * height / width
                # 计算新的高度
                new_height = int(288 * ratio)
                new_size = (288, new_height)
                # 缩放图像
                if new_height >= 288:
                    thumbnail_size = (0,0,288,288)
                else:
                    thumbnail_size = (0,0,new_height,new_height)
                    
                out = img.resize(new_size, Image.ANTIALIAS)
                thumbnail = out.crop(thumbnail_size)
                thumbnail.save(MEDIA_ROOT + filepath_thumbnail)
                corporation.thumbnail = MEDIA_URL + filepath_thumbnail
                out.save(MEDIA_ROOT + filepath)
                corporation.logo = MEDIA_URL + filepath
                
            corporation.save()
            return HttpResponseRedirect('/corporation/' + str(url_number) + '/')
    else:
        form = ModifyCorporationForm()
        return render_to_response('corporation/corporation_manage_edit.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def corporation_manage_members(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    return render_to_response('corporation/corporation_manage_members.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def corporation_manage_advance(request,url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    return render_to_response('corporation/corporation_manage_advance.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def corporation_manage_department(request,url_number):
    from accounts.models import Student
    corporation = Corporation.objects(url_number=url_number).get()
    if request.method == "POST":
        if "user_url_number" in request.POST:
            form_move = MoveMemberForm(request.POST)
            if form_move.is_valid():
                department_name = form_move.cleaned_data['department_name']
                user_url_number = form_move.cleaned_data['user_url_number']
                user = Student.objects(url_number=user_url_number).get()
                sccard = S_C_Card.objects(user=user,corporation=corporation).get()
                corporation.delete_member_from_department(sccard.department,user_url_number)
                corporation.add_member_to_department(department_name,user_url_number)
                return HttpResponseRedirect('')
            
        elif "creat_department" in request.POST:
            form_creat = CreatDepartmentForm(request.POST)
            if form_creat.is_valid():
                department_name = form_creat.cleaned_data['department_name']
                corporation.creat_department(department_name)
                return HttpResponseRedirect('')
            
        elif "delete_department" in request.POST:
            form_delete = DeleteDepartmentForm(request.POST)
            if form_delete.is_valid():
                department_name = form_delete.cleaned_data['department_name']
                corporation.delete_department(department_name)
                return HttpResponseRedirect('')
        
    else:
        form_move = MoveMemberForm()
        form_creat = CreatDepartmentForm()
        form_delete = DeleteDepartmentForm()
        return render_to_response('corporation/corporation_manage_department.html', {'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def demote(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.demote(user_url_number)
    return HttpResponse('success')
    
    
def promote(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.promote(user_url_number)
    return HttpResponse('success')
    
def kick_out(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.kick_out(user_url_number)
    return HttpResponse('success')
    
@login_required(login_url='/')
def redirect_to_topics(request, url_number):
    return HttpResponseRedirect('/corporation/' + str(url_number) + '/structure/')

def visit_corporation_topics(request, gurl_number):
    corporation = Corporation.objects(url_number=gurl_number).get()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topic = Topic(title=title)
            turl_number = len(Topic.objects) + 1
            topic.url_number = turl_number
            topic.content = content
            topic.creat_time = datetime.datetime.now()
            topic.is_active = True
            topic.is_locked = False
            topic.is_top = False
            topic.clicks = 0
            topic.update_time = datetime.datetime.now()
            topic.update_author = request.user
            sccard = S_C_Card.objects(user=request.user, corporation=corporation).get()
            topic.creator = sccard
            topic.save()
            return HttpResponseRedirect('/corporation/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
            
            
    else:
        form = NewTopicForm()
        return render_to_response('corporation/corporation_topics.html', {'form':form, 'corporation':corporation, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
        
def visit_corporation_structure(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    if request.method == "POST":
        form = NewAskForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            creator = [a[0] for a in [S_S_Card.objects.get_or_create(user=request.user, target=admin) for admin in corporation.get_user_admin()]]
            url_number = len(Sitemail.objects) + 1
            mail = Sitemail(title='入社申请', content=content, creator=creator, creat_time=datetime.datetime.now(), is_readed=False, url_number=url_number).save()
            S_C_Card(user=request.user,corporation=corporation,is_active=False,is_admin=False).save()
            return HttpResponse('success')
            
            
    else:
        form = NewAskForm()
        return render_to_response('corporation/corporation_structure.html', {'form':form,'current_user':request.user, 'url_number':url_number, 'corporation':corporation, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

  

def delete(request,corporation_url_number,user_url_number):
    from accounts.models import Student
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    user = Student.objects(url_number=user_url_number).get()
    S_C_Card.objects(user=user, corporation=corporation).delete()
    return HttpResponse('success')
    
def approve(request,corporation_url_number,user_url_number):
    corporation = Corporation.objects(url_number=corporation_url_number).get()
    corporation.entercorporation(user_url_number)
    return HttpResponse('success')
      
def ask_quitcorporation(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    if request.method == "POST":
        form = NewAskForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            creator = S_S_Card.objects.get_or_create(user=request.user, target__in=corporation.get_user_admin)
            url_number = len(Sitemail.objects) + 1
            mail = Sitemail(title='退社申请', content=content, creator=creator, creat_time=datetime.datetime.now(), is_readed=False, url_number=url_number).save()
            return HttpResponse('success')
        
    else:
        return HttpResponse('success')
    

def visit_corporation_activity(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    sccard = S_C_Card.objects(corporation=corporation,user=request.user).get()
    if request.method == "POST":
        form = CreatActivityForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            start_time = form.cleaned_data['start_time']
            finish_time = form.cleaned_data['finish_time']
            place = form.cleaned_data['place']
            max_student = form.cleaned_data['max_student']
            pay = form.cleaned_data['pay']
            detail = form.cleaned_data['detail']
            aurl_number = len(Activity.objects) + 1
            activity = Activity(creator=sccard,url_number=aurl_number,name=name,start_time=start_time,finish_time=finish_time,place=place,max_student=max_student,pay=pay,detail=detail,clicks = 0).save()
            return HttpResponseRedirect('/corporation/' + str(url_number) + '/activity/' + str(aurl_number) + '/')
            
    else:
        form = CreatActivityForm()
        return render_to_response('corporation/corporation_activity.html', {'form':form, 'current_user':request.user, 'url_number':url_number, 'corporation':corporation, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))
  
    
def watch_corporation(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    corporation.watch_corporation(request.user)
    return HttpResponse('success')

    
    
def cancle_watch_corporation(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    corporation.diswatch_corporation(request.user)
    return HttpResponse('success')
    
    
def topic_inactive(request, url_number):
    corporation = Corporation.objects(url_number=url_number).get()
    return render_to_response('corporation/corporation_topics_inactive.html',{'current_user':request.user, 'url_number':url_number, 'corporation':corporation, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))
    
    
    
    
    
    
    
