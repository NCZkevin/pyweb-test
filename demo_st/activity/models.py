# -*- coding: UTF-8 -*-
from mongoengine import Document, fields, PULL
from accounts.models import Student
from mongoengine import signals
import datetime
# Create your models here.



class Activity(Document):
    url_number = fields.IntField()
    name = fields.StringField(verbose_name=u'活动名称')
    detail = fields.StringField(verbose_name=u'活动详情')
    creator = fields.GenericReferenceField() # 发起社团
    
    start_time = fields.DateTimeField()
    finish_time = fields.DateTimeField()
    place = fields.StringField(verbose_name=u'活动地点')
    max_student = fields.IntField()  # 人数上限
    
    pay = fields.IntField(verbose_name=u'人均花费')
    
    who_likes = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))  # 喜欢活动的人
    who_entered = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))  # 参加这个活动的人
    clicks = fields.IntField()  # 点击数
    is_active = fields.BooleanField()
    
    def description(self):
        return self.creator.corporation.name + "发起了" + self.name

    
    
    def is_started(self):  # 判断是否已经开始
        if self.finish_time < datetime.datetime.now():
            return True
        else:
            return False
        
        
    def get_reply(self):
        from reply.models import Reply
        return Reply.objects(target=self)
    
signals.post_save.connect(Student.add_to_allbroadcast, sender=Activity)
        
    
