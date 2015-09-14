'''
Created on 2013-2-4

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('group.views',
    url(r'^my_groups_news/$','my_groups_news'),
    url(r'^my_groups_reply/$','my_groups_reply'),
    url(r'^my_groups_creat/$','my_groups_creat'),
    url(r'^creat_group/$', 'creat_group'),
    url(r'^(\d+)/$', 'group'),
    url(r'^(\d+)/structure/$','visit_group_structure'),
    url(r'^(\d+)/enter/$', 'entergroup'),
    url(r'^(\d+)/quit/$', 'quitgroup'),
    url(r'^(\d+)/topic/(\d+)/$', 'showtopic'),
    url(r'^(\d+)/ask/$','ask_for_admin'),
    url(r'^(\d+)/topic_inactive/$','topic_inactive'),
    url(r'^(\d+)/manage_edit/$','group_manage_edit'),
    url(r'^(\d+)/manage_members/$','group_manage_members'),
    url(r'^(\d+)/manage_advance/$','group_manage_advance'),
    url(r'^(?P<group_url_number>\d+)/promote/(?P<user_url_number>\d+)/$','promote'),
    url(r'^(?P<group_url_number>\d+)/demote/(?P<user_url_number>\d+)/$','demote'),
    url(r'^(?P<group_url_number>\d+)/kick_out/(?P<user_url_number>\d+)/$','kick_out'),
)
