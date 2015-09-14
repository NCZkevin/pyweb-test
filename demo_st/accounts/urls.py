'''
Created on 2013-1-29

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('accounts.views',
    url(r'^$', 'index'),
    url(r'^edit_profile/$', 'signup_profile'),
    url(r'^logout/$', 'userlogout'),
    # url(r'^accounts/$',),
    url(r'^people/(\d+)/$', 'redirect_to_feeds'),
    url(r'^people/(\d+)/feeds/$', 'visit_people_feeds'),
    url(r'^people/(\d+)/profile/$', 'visit_people_profile'),
    url(r'^people/(\d+)/corporation/$', 'visit_people_corporation'),
    url(r'^people/(\d+)/group/$', 'visit_people_group'),
    url(r'^people/(\d+)/add_watch_student/$', 'add_watch_student'),
    url(r'^people/(\d+)/cancle_watch_student/$', 'cancle_watch_student'),
    #url(r'^find/',''),
)

