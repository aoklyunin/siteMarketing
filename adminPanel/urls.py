from django.conf.urls import url

from adminPanel.views import *

urlpatterns = [
    url(r'^replenish/$', replenish),
    url(r'^replenish/list/(?P<state>[0-9]+)/$', replenishList),
    url(r'^withdraw/$', withdraw),
    url(r'^withdraw/list/(?P<state>[0-9]+)/$', withdrawList),
    url(r'^replenish/reject/(?P<tid>[0-9]+)/$', replenishReject),
    url(r'^replenish/accept/(?P<tid>[0-9]+)/$', replenishAccept),
    url(r'^withdraw/reject/(?P<tid>[0-9]+)/$', withdrawReject),
    url(r'^withdraw/accept/(?P<tid>[0-9]+)/$', withdrawAccept),
    url(r'^campany/dismiss/(?P<tid>[0-9]+)/$', dismissCampany),
    url(r'^', index, name='index')
]
