# -*- coding: UTF-8 -*-   
from accounts.models import Student
from mongoengine import Document, fields, DO_NOTHING
# Create your models here.
class Topic(Document):
    title = fields.StringField(verbose_name=u'标题')
    content = fields.StringField(verbose_name=u'内容')
    url_number = fields.IntField()
    
    creator = fields.GenericReferenceField()  # 发布人S_G_Card, reverse_delete_rule=DO_NOTHING
    creat_time = fields.DateTimeField()  # 发布时间
    
    update_time = fields.DateTimeField()  # 更新时间
    update_author = fields.ReferenceField(Student, reverse_delete_rule=DO_NOTHING)  #最后回复作者
    
    clicks = fields.IntField()  #浏览数
    
    is_active = fields.BooleanField(verbose_name=u'可见')
    is_locked = fields.BooleanField(verbose_name=u'锁帖')
    is_top = fields.BooleanField(verbose_name=u'置顶')
    
    def get_reply(self):
        from reply.models import Reply
        return Reply.objects(target=self)
    


    

