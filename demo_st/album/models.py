from mongoengine import Document, fields, CASCADE
from corporation.models import Corporation
# Create your models here.
class Poster(Document):
    corporation = fields.ReferenceField(Corporation, reverse_delete_rule=CASCADE)
    creat_time = fields.DateTimeField()


class Photo(Document):
    description = fields.StringField()
    image = fields.ImageField()
    poster = fields.ReferenceField(Poster, reverse_delete_rule=CASCADE)

