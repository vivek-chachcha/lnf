"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^signup/$', views.signUpUser, name= 'SignUp'),
    url(r'^profile/$', views.getProfile, name= 'Profile'),
    url(r'^login/$', views.loginUser, name= 'Login'),
    url(r'^logout/$', views.logoutUser, name= 'Logout'),
    url(r'^error/$', views.error, name='error'),
    url(r'^createpost/$', views.createpost, name='createpost',),
    url(r'^(?P<post_id>[0-9]+)/post/$', views.post, name='post'),
    url(r'^lostposts/list$', views.posts, name='lostpostslist'),
    url(r'^foundposts/list$', views.posts, name='foundpostslist'),
    url(r'^lostposts/map$', views.posts, name='lostpostsmap'),
    url(r'^foundposts/map$', views.posts, name='foundpostsmap'),
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^admin/import', views.importData, name='importdata'),
    url(r'^admin/startimport', views.importDataStart, name='importdatastart'),
    url(r'^(?P<post_id>[0-9]+)/edit/$', views.edit, name='edit'),
]
