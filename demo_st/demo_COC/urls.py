from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo_COC.views.home', name='home'),
    # url(r'^demo_COC/', include('demo_COC.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'', include('accounts.urls')),
    # url(r'^accounts/',include('accounts.urls')),
    # url(r'^people/', include('accounts.urls')),
    url(r'^group/', include('group.urls')),
    url(r'^corporation/',include('corporation.urls')),
    url(r'^topic/',include('topic.urls')),
    url(r'^sitemail/',include('sitemail.urls')),
    url(r'^find/',include('find.urls')),
)

