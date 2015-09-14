'''
Created on 2013-3-25

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('sitemail.views',
    url(r'^inbox/$','inbox'),
    url(r'^outbox/$','outbox'),
    url(r'^(\d+)/$','showmail'),
    url(r'^sendmail/$','sendmail'),
)