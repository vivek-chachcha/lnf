from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^allPosts/$', views.allPosts, name='allPosts'),
    url(r'^createPost/$', views.createPost, name='createPost',),
    url(r'^(?P<post_id>[0-9]+)/post/$', views.post, name='post'),

]