from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.create),
    url(r'^users/(?P<user_id>\d+)$', views.show),
    url(r'^logout$', views.logout),
]