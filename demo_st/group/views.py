# -*- coding: UTF-8 -*-
import os
import datetime
from PIL import Image
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from demo_COC.settings import STATIC_URL, MEDIA_ROOT, MEDIA_URL
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from forms import CreatGroupForm,ModifyGroupForm
from models import Group
from reply.models import Reply
from reply.forms import NewReplyForm
from topic.models import Topic
from topic.forms import NewTopicForm, ModifyTopicForm
from relations.models import S_G_Card
from django.template import RequestContext
from mongoengine.django.sessions import MongoSession
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def creat_group(request):
    if request.method == "POST":
        form = CreatGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            grouptype = form.cleaned_data['grouptype']
            group = Group(name=name, introduction=introduction, grouptype=grouptype, logo=STATIC_URL + 'img/face.png', thumbnail=STATIC_URL + 'img/face.png')
            url_number = len(Group.objects) + 1
            group.url_number = url_number
            group.birthday = datetime.datetime.now()
            if request.FILES:
                path = 'img/group/' + str(url_number)
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
                group.thumbnail = MEDIA_URL + filepath_thumbnail
                out.save(MEDIA_ROOT + filepath)
                group.logo = MEDIA_URL + filepath
                
            group.save()
            sgcard = S_G_Card(user=request.user, group=group, is_active=True, is_admin=True,creat_time=datetime.datetime.now())
            sgcard.save()
            return HttpResponseRedirect('/group/' + str(url_number) + '/')
        
    else:
        form = CreatGroupForm()
        return render_to_response('group/creat_group.html', {'form':form, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
                
                 
def group(request, gurl_number):
    group = Group.objects(url_number=gurl_number).get()
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
            sgcard = S_G_Card.objects(user=request.user, group=group).get()
            topic.creator = sgcard
            topic.save()
            return HttpResponseRedirect('/group/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
            
            
    else:
        form = NewTopicForm()
        return render_to_response('group/group.html', {'form':form, 'group':group, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
        
    
def entergroup(request, url_number):
    group = Group.objects(url_number=url_number).get()
    group.entergroup(request.user)
    return HttpResponse('success')
    
def quitgroup(request, url_number):
    group = Group.objects(url_number=url_number).get()
    group.quitgroup(request.user)
    return HttpResponse('success')
    
    
def showtopic(request, gurl_number, turl_number):
    group = Group.objects(url_number=gurl_number).get()
    topic = Topic.objects(url_number=turl_number).get()
    topic.clicks = topic.clicks + 1
    topic.save()
    if request.method == 'POST':
        if "reply" in request.POST:
            reply_form = NewReplyForm(request.POST)
            if reply_form.is_valid():
                content = reply_form.cleaned_data['content']
                reply = Reply(content=content)
                sgcard = S_G_Card.objects(user=request.user, group=group).get()
                reply.creator = sgcard
                reply.creat_time = datetime.datetime.now()
                reply.target = topic
                reply.is_active = True
                reply.save()
                topic.update_author = request.user
                topic.update_time = datetime.datetime.now()
                topic.clicks = topic.clicks - 1
                topic.save()
                return HttpResponseRedirect('/group/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
            
        if "modify" in request.POST:
            modify_form = ModifyTopicForm(request.POST)
            if modify_form.is_valid():
                content = modify_form.cleaned_data['content']
                topic.content = content
                topic.clicks = topic.clicks - 1
                topic.save()
                return HttpResponseRedirect('/group/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
        
    else:
        reply_form = NewReplyForm()
        modify_form = ModifyTopicForm()
        topic.clicks = topic.clicks + 1
        topic.save()
        return render_to_response('group/group_topic.html', {'group':group, 'current_user':request.user, 'reply_form':reply_form, 'topic':topic, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

    
def my_groups_creat(request):
    return render_to_response('group/my_groups_creat.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def my_groups_news(request):
    return render_to_response('group/my_groups_news.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))

def my_groups_reply(request):
    return render_to_response('group/my_groups_reply.html', {'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def ask_for_admin(request,url_number):
    group = Group.objects(url_number=url_number).get()
    group.ask_for_admin(request.user)
    return HttpResponse('success')
                
                
def group_manage_edit(request,url_number):
    group = Group.objects(url_number=url_number).get()
    if request.method == "POST":
        form = ModifyGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            group.update(set__name=name, set__introduction=introduction)
            if request.FILES:
                path = 'img/group/' + str(url_number)
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
                group.thumbnail = MEDIA_URL + filepath_thumbnail
                out.save(MEDIA_ROOT + filepath)
                group.logo = MEDIA_URL + filepath
                
            group.save()
            return HttpResponseRedirect('/group/' + str(url_number) + '/')
    else:
        form = ModifyGroupForm()
        return render_to_response('group/group_manage_edit.html', {'group':group, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def group_manage_members(request,url_number):
    group = Group.objects(url_number=url_number).get()
    return render_to_response('group/group_manage_members.html', {'group':group, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def group_manage_advance(request,url_number):
    group = Group.objects(url_number=url_number).get()
    return render_to_response('group/group_manage_advance.html', {'group':group, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def topic_inactive(request,url_number):
    group = Group.objects(url_number=url_number).get()
    return render_to_response('group/group_topic_inactive.html', {'group':group, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
def visit_group_structure(request,url_number):
    group = Group.objects(url_number=url_number).get()
    return render_to_response('group/group_structure.html', {'group':group, 'STATIC_URL':STATIC_URL, 'current_user':request.user}, context_instance=RequestContext(request))
  
  
def demote(request,group_url_number,user_url_number):
    group = Group.objects(url_number=group_url_number).get()
    group.demote(user_url_number)
    return HttpResponse('success')
    
    
def promote(request,group_url_number,user_url_number):
    group = Group.objects(url_number=group_url_number).get()
    group.promote(user_url_number)
    return HttpResponse('success')
    
def kick_out(request,group_url_number,user_url_number):
    group = Group.objects(url_number=group_url_number).get()
    group.kick_out(user_url_number)
    return HttpResponse('success')
    
    
    
