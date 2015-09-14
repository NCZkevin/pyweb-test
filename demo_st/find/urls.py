'''
Created on 2013-3-27

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('find.views',
    url(r'^$','find_corporation'),
    url(r'^group/$','find_group'),
    url(r'^corporation/$','find_corporation'),
    url(r'^topic/$','find_topic'),
    url(r'^activity/$','find_activity'),
)