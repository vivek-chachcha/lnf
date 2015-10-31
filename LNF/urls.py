from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^createpost/$', views.createpost, name='createpost',),
    url(r'^(?P<post_id>[0-9]+)/post/$', views.post, name='post'),

]