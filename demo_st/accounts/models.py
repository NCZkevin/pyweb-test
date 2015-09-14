# -*- coding: UTF-8 -*-
from mongoengine.django.auth import User
from mongoengine import fields, EmbeddedDocument, Document, signals




class Public_Profile(EmbeddedDocument):
    realname = fields.StringField()
    face = fields.StringField()
    thumbnail = fields.StringField()
    gender = fields.StringField(max_length=2)
    school = fields.StringField()
    birthday = fields.DateTimeField()

class Private_Profile(EmbeddedDocument):
    phone_number = fields.StringField()
    major = fields.StringField()
    MBTI = fields.StringField()


class Broadcast(EmbeddedDocument):
    object = fields.GenericReferenceField()
    is_readed = fields.BooleanField()


class Student(User):
    url_number = fields.IntField()
    public_profile = fields.EmbeddedDocumentField(Public_Profile)
    private_profile = fields.EmbeddedDocumentField(Private_Profile)
    mybroadcast = fields.ListField(fields.EmbeddedDocumentField(Broadcast))
    allbroadcast = fields.ListField(fields.EmbeddedDocumentField(Broadcast))
    alerts = fields.ListField(fields.EmbeddedDocumentField(Broadcast))

    def find_group(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(group__nin=self.get_group_all())
    
    def find_corporation(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(corporation__nin=self.get_corporation_all())
    
    def find_topic(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.find_group())
    
    def find_activity(self):
        from activity.models import Activity
        return Activity.objects(creator__nin=self.get_corporation_active())
    
    
    
    
    def get_fans(self):
        return self.get_sscard_as_target().scalar('user')
    
    def get_watchpeople(self):
        return self.get_sscard_as_user().scalar('target')
    
    
    #############################################################对关系卡 的操作#########################################################
    
    
    ###################################################对SS卡 的操作
    def get_sscard_as_user(self):
        from relations.models import S_S_Card
        return S_S_Card.objects(user=self)
    
    def get_sscard_as_target(self):
        from relations.models import S_S_Card
        return S_S_Card.objects(target=self)
    
    
    ###################################################对SG卡 的操作
    def get_sgcard_all(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(user=self)
    
    def get_sgcard_active(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(user=self, is_active=True)
    
    def get_sgcard_inactive(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(user=self, is_active=False)
    
    def get_sgcard_admin(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(user=self, is_active=True, is_admin=True)
    
    def get_sgcard_not_admin(self):
        from relations.models import S_G_Card
        return S_G_Card.objects(user=self, is_active=True, is_admin=False)
    
    
    ###################################################对SC卡 的操作
    def get_sccard_all(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(user=self)
    
    def get_sccard_active(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(user=self, is_active=True)
    
    def get_sccard_inactive(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(user=self, is_active=False)
    
    def get_sccard_admin(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(user=self, is_active=True, is_admin=True)
    
    def get_sccard_not_admin(self):
        from relations.models import S_C_Card
        return S_C_Card.objects(user=self, is_active=True, is_admin=False)
    
    
    
    
    #############################################################对Group的操作#########################################################
    def get_group_all(self):
        return self.get_sgcard_all().scalar('group')
    
    def get_group_active(self):
        return self.get_sgcard_active().scalar('group')
    
    def get_group_inactive(self):
        return self.get_sgcard_inactive().scalar('group')
    
    def get_group_admin(self):#得到管理的小组
        return self.get_sgcard_admin().scalar('group')
    
    def get_group_not_admin(self):#得到参与的小组
        return self.get_sgcard_not_admin().scalar('group')
    
    
    
    
    #############################################################对Corporation的操作#########################################################
    def get_corporation_all(self):
        return self.get_sccard_all().scalar('corporation')
    
    def get_corporation_active(self):
        return self.get_sccard_active().scalar('corporation')
    
    def get_corporation_inactive(self):
        return self.get_sccard_inactive().scalar('corporation')
    
    def get_corporation_admin(self):#得到管理的社团
        return self.get_sccard_admin().scalar('corporation')
    
    def get_corporation_not_admin(self):#得到加入的社团
        return self.get_sccard_not_admin().scalar('corporation')
    
    
    
    
    
    #############################################################对Topic的操作#########################################################

    
    ###################################################对Group Topic的操作
    def get_topic_group_active(self):#我关注的小组的话题
        from topic.models import Topic
        from relations.models import S_G_Card
        return Topic.objects(creator__in=S_G_Card.objects(group__in=self.get_group_active()), is_active=True)
    
    def get_topic_group_creat_active(self):#我创建的小组话题(active)
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=True)

    def get_topic_group_creat_inactive(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sgcard_all(), is_active=False)

    def get_topic_group_reply_active(self):#我回复的小组话题(active)
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sgcard_all(), is_active=True).distinct('target')


    ###################################################对Corporation Topic的操作
    def get_topic_corporation_active(self):#我关注的小组的话题
        from topic.models import Topic
        from relations.models import S_C_Card
        return Topic.objects(creator__in=S_C_Card.objects(corporation__in=self.get_corporation_active()), is_active=True)
    
    def get_topic_corporation_creat_active(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=True)

    def get_topic_corporation_creat_inactive(self):
        from topic.models import Topic
        return Topic.objects(creator__in=self.get_sccard_all(), is_active=False)

    def get_topic_corporation_reply_active(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sccard_all(), is_active=True).distinct('target')

    #############################################################对Activity的操作#########################################################

    ###################################################对Corporation Topic的操作
    def get_activity_corporation_creat_active(self):
        from activity.models import Activity
        return Activity.objects(creator__in=self.get_sccard_all(), is_active=True)

    def get_activity_corporation_creat_inactive(self):
        from activity.models import Activity
        return Activity.objects(creator__in=self.get_sccard_all(), is_active=False)

    def get_activity_corporation_reply_active(self):
        from reply.models import Reply
        from activity.models import Activity
        return Reply.objects(creator__in=self.get_sccard_all(), is_active=True).distinct('target')

    #############################################################对Reply的操作#########################################################

    ###################################################对Group Reply的操作
    def get_reply_group_creat_active(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sgcard_all(), is_active=True)

    def get_reply_group_creat_inactive(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sgcard_all(), is_active=False)

    def get_reply_group_reply_active(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sgcard_all(), is_active=True).distinct('target')

    ###################################################对Corporation Reply的操作
    def get_reply_corporation_creat_active(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sccard_all(), is_active=True)

    def get_reply_corporation_creat_inactive(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sccard_all(), is_active=False)

    def get_reply_corporation_reply_active(self):
        from reply.models import Reply
        return Reply.objects(creator__in=self.get_sccard_all(), is_active=True).distinct('target')

    ###################################################对sitemail的操作
    def get_inbox(self):
        from sitemail.models import Sitemail
        return Sitemail.objects(creator__in=self.get_sscard_as_target())

    def get_outbox(self):
        from sitemail.models import Sitemail
        return Sitemail.objects(creator__in=self.get_sscard_as_user())
    
    def get_inbox_not_readed(self):
        from sitemail.models import Sitemail
        return Sitemail.objects(creator__in=self.get_sscard_as_target(), is_readed=False)

    def get_inbox_readed(self):
        from sitemail.models import Sitemail
        return Sitemail.objects(creator__in=self.get_sscard_as_target(), is_readed=True)








    def like(self, document):
        self.update(push__mybroadcast=document)
        self.get_fans().update(push__allbroadcast=document)
    
    
    
    @classmethod
    def add_to_mybroadcast(cls, sender, document, **kwargs):
        broadcast = Broadcast(object=document, is_readed=False)
        document.user.update(push__mybroadcast=broadcast)
        
    @classmethod
    def add_to_allbroadcast(cls, sender, document, **kwargs):
        from relations.models import S_C_Card, S_G_Card
        from activity.models import Activity
        broadcast = Broadcast(object=document, is_readed=False)
        if sender == S_C_Card or sender == S_G_Card:
            for user in document.user.get_fans():
                user.update(push__allbroadcast=broadcast)
        elif sender == Activity:
            [user.update(push__allbroadcast=broadcast) for user in document.creator.corporation.who_watches]
        elif sender == Feeds:
            for user in document.user.get_fans():
                user.update(push__allbroadcast=broadcast)
            document.user.update(push__allbroadcast=broadcast)
            
    @classmethod
    def add_alert_sitemail(cls, sender, document, **kwargs):
        broadcast = Broadcast(object=document, is_readed=False)
        document.creator.target.update(push__alerts=broadcast)
        
    @classmethod
    def add_alert_reply(cls, sender, document, **kwargs):
        broadcast = Broadcast(object=document, is_readed=False)
        document.target.creator.user.update(push__alerts=broadcast)



    def get_mybroadcast_length(self):
        return len(self.mybroadcast)

    def get_allbroadcast_length(self):
        return len(self.allbroadcast)
    
    def get_alerts_length(self):
        return len(self.alerts)
    
class Feeds(Document):
    user = fields.ReferenceField(Student)
    content = fields.StringField()
    creat_time = fields.DateTimeField()
    
    def description(self):
        return self.content
    

signals.post_save.connect(Student.add_to_allbroadcast, sender=Feeds)
signals.post_save.connect(Student.add_to_mybroadcast, sender=Feeds)
    
    
    
    
    
    
    


