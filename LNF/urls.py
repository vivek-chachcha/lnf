from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^posts/$', views.PostView.as_view(), name='posts'),
]