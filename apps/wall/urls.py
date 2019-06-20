from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.wall, name='myWall'),
    url(r'^postMessage$', views.postMessage, name="postMessage"),
    url(r'^postComment$', views.postComment, name="postComment"),
    url(r'^deleteMessage/(?P<id>\d+)$', views.deleteMessage, name="deleteMess")

]
