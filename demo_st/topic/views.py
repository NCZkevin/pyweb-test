from models import Topic
from django.http import HttpResponse, HttpResponseRedirect



def about_top(request, turl_number):
    topic = Topic.objects(url_number=turl_number).get()
    if topic.is_top:
        topic.update(set__is_top=False)
    else:
        topic.update(set__is_top=True)
        
    return HttpResponse('success')
        
def about_lock(request, turl_number):
    topic = Topic.objects(url_number=turl_number).get()
    if topic.is_locked:
        topic.update(set__is_locked=False)
    else:
        topic.update(set__is_locked=True)
        
    return HttpResponse('success')

def about_active(request, turl_number):
    topic = Topic.objects(url_number=turl_number).get()
    if topic.is_active:
        topic.update(set__is_active=False)
    else:
        topic.update(set__is_active=True)
        
    return HttpResponse('success')

