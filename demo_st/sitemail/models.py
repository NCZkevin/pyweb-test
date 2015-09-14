# -*- coding: UTF-8 -*-
from relations.models import S_S_Card
from mongoengine import Document, fields, signals, CASCADE
from reply.models import Reply
# Create your models here.
class Sitemail(Document):
    url_number = fields.IntField()
    title = fields.StringField()
    content = fields.StringField()
    creat_time = fields.DateTimeField()
    creator = fields.ListField(fields.ReferenceField(S_S_Card, reverse_delete_rule=CASCADE))
    is_readed = fields.BooleanField()

    def get_reply(self):#得到回复列表
        return Reply.objects(target=self)



