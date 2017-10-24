from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.new),
    url(r'^(?P<book_id>\d+)$', views.show),
    url(r'^create_book$', views.create_book),
    url(r'^add_review$', views.add_review),
]