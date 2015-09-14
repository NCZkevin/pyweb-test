'''
Created on 2013-3-22

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('topic.views',
    url(r'^(\d+)/about_top/$','about_top'),
    url(r'^(\d+)/about_lock/$','about_lock'),
    url(r'^(\d+)/about_active/$','about_active'),
)