# -*- coding: UTF-8 -*-
from mongoengine import Document, fields
# Create your models here.
class Reply(Document):
    content = fields.StringField(verbose_name=u'内容')
    creator = fields.GenericReferenceField()#作者
    target = fields.GenericReferenceField()#回复目标
    creat_time = fields.DateTimeField()#发布时间
    is_active = fields.BooleanField(verbose_name=u'可见')
    
    
    def get_reply(self):#得到回复列表
        return Reply.objects(target=self)
    