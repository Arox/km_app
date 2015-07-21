from django.conf.urls import patterns, url
from clients.views import ClientCreate, ClientUpdate, ClientsView, ClientDetail, ClientDelete, ClientLikes

urlpatterns = patterns('',
    #url(r'^$', views.list_objects),
    url(r'^/create', ClientCreate.as_view(), name="create"),
    url(r'^/update/(?P<pk>\d+)$', ClientUpdate.as_view(), name="update"),
    url(r'^/delete/(?P<pk>\d+)$', ClientDelete.as_view(), name="delete"),
    url(r'^/client/(?P<pk>\d+)$', ClientDetail.as_view(), name="detail"),
    url(r'^/likes', ClientLikes.as_view(), name="likes"),
    url(r'^[/\?(?P<name>\w*)]?$', ClientsView.as_view(), name="view"),
)