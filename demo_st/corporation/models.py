# -*- coding: UTF-8 -*-
from mongoengine import Document, fields, PULL
from accounts.models import Student
import datetime

# Create your models here.

class Corporation(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True, verbose_name=u'社团名称')
    logo = fields.StringField()  # logo路径
    thumbnail = fields.StringField()
    birthyear = fields.IntField()  # 创建年份
    creat_time = fields.DateTimeField()
    departments = fields.ListField(fields.StringField())#部门
    introduction = fields.StringField(required=True, verbose_name=u'社团简介')
    #tags = fields.ListField(fields.StringField())  # 社团标签
    school = fields.StringField()#学校
    who_watches = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))#关注它的人
    
    #社团管理
    
    def creat_department(self, department_name):#创建部门
        return self.update(push__departments=department_name)
    
    def delete_department(self, department_name):#删除部门
        for sccard in self.get_sccard_active():
            if sccard.department == department_name:
                sccard.update(set__department="")
            
        return self.update(pull__departments=department_name)
    
    def add_member_to_department(self, department_name, user_url_number):
        user = Student.objects(url_number=user_url_number).get()
        from relations.models import S_C_Card
        return S_C_Card.objects(user=user, corporation=self).update(set__department=department_name)
    
    def delete_member_from_department(self, department_name, user_url_number):
        user = Student.objects(url_number=user_url_number).get()
        from relations.models import S_C_Card
        return S_C_Card.objects(user=user, corporation=self).update(set__department="")
    
    
    #降低权限
    def demote(self,user_url_number):
        from relations.models import S_C_Card
        user = Student.objects(url_number=user_url_number).get()
        S_C_Card.objects(corporation=self, user=user).update(set__is_admin=False)
    
    #提升权限
    def promote(self,user_url_number):
        from relations.models import S_C_Card
        user = Student.objects(url_number=user_url_number).get()
        S_C_Card.objects(corporation=self, user=user).update(set__is_admin=True)
    
    #踢出社团
    def kick_out(self,user_url_number):
        from relations.models import S_C_Card
        user = Student.objects(url_number=user_url_number).get()
        S_C_Card.objects(corporation=self, user=user).update(set__is_active=False)
        
            
    #申请加入社团
    def entercorporation(self, user_url_number):
        from accounts.models import Student
        user = Student.objects(url_number=user_url_number).get()
        from relations.models import S_C_Card
        if self.get_user_admin():
            if S_C_Card.objects(user=user, corporation=self):
                S_C_Card.objects(user=user, corporation=self).update(set__is_active=True, set__is_admin=False, set__creat_time=datetime.datetime.now())
            else:
                S_C_Card(user=user, corporation=self, is_active=True, is_admin=False, creat_time=datetime.datetime.now()).save()
        else:
            if S_C_Card.objects(user=user, corporation=self):
                S_C_Card.objects(user=user, corporation=self).update(set__is_active=True, set__is_admin=True, set__creat_time=datetime.datetime.now())
            else:
                S_C_Card(user=user, corporation=self, is_active=True, is_admin=True, creat_time=datetime.datetime.now()).save()
        
    #退出社团
    def quitcorporation(self, user_url_number):
        from accounts.models import Student
        user = Student.objects(url_number=user_url_number).get()
        from relations.models import S_C_Card
        S_C_Card.objects(user=user, corporation=self, is_active=True).update(set__is_active=False)
        

    #关注社团
    def watch_corporation(self, user):
        return self.update(push__who_watches=user)

    #取消关注
    def diswatch_corporation(self, user):
        return self.update(pull__who_watches=user)

    
    #查询sccard
    def get_sccard_all(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(corporation=self)
    
    def get_sccard_active(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True)
        
    def get_sccard_inactive(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=False)
    
    def get_sccard_admin(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True, is_admin=True)
    
    def get_sccard_not_admin(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True, is_admin=False)
    
    
    #查询user
    def get_user_all(self):
        return self.get_sccard_all().scalar('user')
    
    def get_user_active(self):
        return self.get_sccard_active().scalar('user')
    
    def get_user_inactive(self):
        return self.get_sccard_inactive().scalar('user')
    
    def get_user_admin(self):
        return self.get_sccard_admin().scalar('user')
    
    def get_user_not_admin(self):
        return self.get_sccard_not_admin().scalar('user')
    
    
    #查询topic
    def get_topic_active(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=True)
    
    def get_topic_inactive(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=False)
    
    def get_topic_top(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=True, is_top=True)
    
    def get_topic_not_top(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=True, is_top=False)
    
    def get_topic_locked(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=True, is_locked=True)
    
    def get_topic_not_locked(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=True, is_locked=False)
    
    
    #查询activity
    def get_activity_active(self):
        from activity.models import Activity
        return Activity.objects(creator__in=self.get_sccard_active())
    
    
    
    
    
    
