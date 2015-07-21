from django.conf.urls import patterns, include, url
from . import view
#from django.contrib import admin

from django.conf import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'km_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^clients', include('clients.urls', namespace='clients', app_name='clients')),
    url(r'^$', view.start),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

    #url(r'^clients/(?P<name>\w+)/', ClientsView.as_view()),
    #url(r'^admin/', include(admin.site.urls)),
)
