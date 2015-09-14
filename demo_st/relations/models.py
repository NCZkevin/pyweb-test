# -*- coding: UTF-8 -*-
from mongoengine import Document, fields, CASCADE, NULLIFY
from mongoengine import signals
from corporation.models import Corporation
from group.models import Group
from accounts.models import Student
# Create your models here.
class S_S_Card(Document):
    user = fields.ReferenceField(Student, reverse_delete_rule=CASCADE ,required=True)
    target = fields.ReferenceField(Student, reverse_delete_rule=CASCADE,required=True)
    
    def description(self):
        return self.user.public_profile.realname + "关注了" + self.target.public_profile.realname
    
    
    

class S_C_Card(Document):
    user = fields.ReferenceField(Student, reverse_delete_rule=NULLIFY)
    department = fields.StringField()#部门
    corporation = fields.ReferenceField(Corporation, reverse_delete_rule=CASCADE)
    creat_time = fields.DateTimeField()#入社时间
    is_active = fields.BooleanField()
    is_admin = fields.BooleanField()#是否是社团管理员
    
    def description(self):
        return self.user.public_profile.realname + "加入了" + self.corporation.name
    
    
    
    #查询topic
    def get_topic_creat_active(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True)
    
    def get_topic_creat_inactive(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=False)
    
    def get_topic_creat_top(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_top=True)
    
    def get_topic_creat_not_top(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_top=False)
    
    def get_topic_creat_locked(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_locked=True)
    
    def get_topic_creat_not_locked(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_locked=False)
    
    def get_topic_reply_active(self):
        from reply.models import Reply
        from topic.models import Topic
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Topic, is_active=True)

    def get_topic_reply_inactive(self):
        from reply.models import Reply
        from topic.models import Topic
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Topic, is_active=False)
    
    
    
    #查询reply
    def get_reply_creat_active(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=True)
    
    def get_reply_creat_inactive(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=False)

    def get_reply_reply_active(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Reply, is_active=True)

    def get_reply_reply_inactive(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Reply, is_active=False)


    
    
    #查询activity
    def get_activity_creat_active(self):
        from activity.models import Activity
        return Activity.objects(creator=self, is_active=True)
    
    def get_activity_creat_inactive(self):
        from activity.models import Activity
        return Activity.objects(creator=self, is_active=False)
    
    def get_activity_reply_active(self):
        from reply.models import Reply
        from activity.models import Activity
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Activity, is_active=True)

    def get_activity_reply_inactive(self):
        from reply.models import Reply
        from activity.models import Activity
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Activity, is_active=False)



class S_G_Card(Document):
    user = fields.ReferenceField(Student, reverse_delete_rule=NULLIFY)
    group = fields.ReferenceField(Group, reverse_delete_rule=CASCADE)
    creat_time = fields.DateTimeField()
    is_active = fields.BooleanField()#保证退出小组之后话题还在
    is_admin = fields.BooleanField()#是否是小组管理员
    
    def description(self):
        return self.user.public_profile.realname + "加入了" + self.group.name

    
    #查询topic
    def get_topic_creat_active(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True)
    
    def get_topic_creat_inactive(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=False)
    
    def get_topic_creat_top(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_top=True)
    
    def get_topic_creat_not_top(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_top=False)
    
    def get_topic_creat_locked(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_locked=True)
    
    def get_topic_creat_not_locked(self):
        from topic.models import Topic
        return Topic.objects(creator=self, is_active=True, is_locked=False)
    
    def get_topic_reply_active(self):
        from reply.models import Reply
        from topic.models import Topic
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Topic, is_active=True)

    def get_topic_reply_inactive(self):
        from reply.models import Reply
        from topic.models import Topic
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Topic, is_active=False)
    
    
    
    #查询reply
    def get_reply_creat_active(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=True)
    
    def get_reply_creat_inactive(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=False)

    def get_reply_reply_active(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Reply, is_active=True)

    def get_reply_reply_inactive(self):
        from reply.models import Reply
        return Reply.objects(creator=self, is_active=True).distinct('target').objects(_cls=Reply, is_active=False)

    
signals.post_save.connect(Student.add_to_allbroadcast, sender=S_G_Card)
signals.post_save.connect(Student.add_to_allbroadcast, sender=S_C_Card)
signals.post_save.connect(Student.add_to_mybroadcast, sender=S_G_Card)
signals.post_save.connect(Student.add_to_mybroadcast, sender=S_C_Card)
