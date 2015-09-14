# -*- coding: UTF-8 -*-
from mongoengine import Document, fields
import datetime
# Create your models here.
class Group(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True, verbose_name=u'小组名称')
    logo = fields.StringField()  # logo路径
    thumbnail = fields.StringField()
    birthday = fields.DateTimeField()  # 创建日期
    introduction = fields.StringField(required=True, verbose_name=u'小组介绍')
    # tags = fields.ListField(fields.StringField())#小组标签
    school = fields.StringField()
    grouptype = fields.StringField()  # 小组类型，是否为私密小组
    
    #得到各种sgcard
    def get_sgcard_all(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(group=self)
    
    def get_sgcard_active(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=True)
    
    def get_sgcard_inactive(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=False)
    
    def get_sgcard_admin(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=True, is_admin=True)
    
    def get_sgcard_not_admin(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(group=self, is_active=True, is_admin=False)
    
    
    #得到各种user
    def get_user_all(self):
        return self.get_sgcard_all().scalar('user')
    
    def get_user_active(self):
        return self.get_sgcard_active().scalar('user')
    
    def get_user_inactive(self):
        return self.get_sgcard_inactive().scalar('user')
    
    def get_user_admin(self):
        return self.get_sgcard_admin().scalar('user')
    
    def get_user_not_admin(self):
        return self.get_sgcard_not_admin().scalar('user')
        
        
    #得到各种topic
    def get_topic_active(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=True)
    
    def get_topic_inactive(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=False)
    
    def get_topic_top(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=True, is_top=True)
    
    def get_topic_not_top(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=True, is_top=False)
    
    def get_topic_locked(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=True, is_locked=True)
    
    def get_topic_not_locked(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=True, is_locked=False)
    
    
    
    #降低权限
    def demote(self,user_url_number):
        from accounts.models import Student
        from relations.models import S_G_Card
        user = Student.objects(url_number=user_url_number).get()
        S_G_Card.objects(group=self,user=user).update(set__is_admin=False)
    
    #提升权限
    def promote(self,user_url_number):
        from accounts.models import Student
        from relations.models import S_G_Card
        user = Student.objects(url_number=user_url_number).get()
        S_G_Card.objects(group=self,user=user).update(set__is_admin=True)
    
    #踢出小组
    def kick_out(self,user_url_number):
        from accounts.models import Student
        from relations.models import S_G_Card
        user = Student.objects(url_number=user_url_number).get()
        S_G_Card.objects(group=self,user=user).update(set__is_active=False)
        
    #申请管理员权限
    def ask_for_admin(self,user):
        from relations.models import S_G_Card
        if not self.get_user_admin():
            S_G_Card.objects(user=user, group=self, is_active=True).update(set__is_admin=True)
            
    
            
            
    #加入小组
    def entergroup(self, user):
        from relations.models import S_G_Card
        if self.get_user_active():
            if S_G_Card.objects(user=user, group=self):
                S_G_Card.objects(user=user, group=self).update(set__is_active=True, set__is_admin=False, set__creat_time=datetime.datetime.now())
            else:
                S_G_Card(user=user, group=self, is_active=True, is_admin=False,creat_time=datetime.datetime.now()).save()
        else:
            if S_G_Card.objects(user=user, group=self):
                S_G_Card.objects(user=user, group=self).update(set__is_active=True, set__is_admin=True,set__creat_time=datetime.datetime.now())
            else:
                S_G_Card(user=user, group=self, is_active=True,is_admin=True, creat_time=datetime.datetime.now()).save()
        
    #退出小组
    def quitgroup(self, user):
        from relations.models import S_G_Card
        S_G_Card.objects(user=user, group=self, is_active=True).update(set__is_active=False)
        
