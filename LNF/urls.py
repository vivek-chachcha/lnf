from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^lostposts/$', views.LostPostView.as_view(), name='lostposts'),
    url(r'^foundposts/$', views.FoundPostView.as_view(), name='foundposts'),
]