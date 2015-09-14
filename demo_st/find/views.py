from django.shortcuts import render_to_response
from demo_COC.settings import STATIC_URL
from django.template import RequestContext
def find_corporation(request):
    return render_to_response('find/find_corporation.html',{'current_user':request.user, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

def find_group(request):
    return render_to_response('find/find_group.html',{'current_user':request.user, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

def find_topic(request):
    return render_to_response('find/find_topic.html',{'current_user':request.user, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))

def find_activity(request):
    return render_to_response('find/find_activity.html',{'current_user':request.user, 'STATIC_URL':STATIC_URL}, context_instance=RequestContext(request))