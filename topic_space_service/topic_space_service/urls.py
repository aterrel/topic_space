from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^topic_space_app/', include('topic_space_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
