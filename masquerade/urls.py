from django.conf.urls import url

from masquerade.views import mask, unmask

urlpatterns = [
    url(r'^mask/$', mask, name='start_masquerading'),
    url(r'^unmask/$', unmask, name='stop_masquerading'),
]
