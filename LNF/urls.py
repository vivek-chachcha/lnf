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
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^error/$', views.error, name='error'),
    url(r'^createpost/$', views.createpost, name='createpost',),
    url(r'^(?P<post_id>[0-9]+)/post/$', views.post, name='post'),
    url(r'^lostposts/$', views.LostPostView, name='lostposts'),
    url(r'^foundposts/$', views.FoundPostView, name='foundposts'),
    url(r'^bmposts/$', views.displayBookmarkedPosts, name='bmposts'),
    url(r'^$', views.HomeView, name='home'),
    url(r'^about/$', views.AboutView, name='about'),
    url(r'^import/$', views.importData, name='import'),
]
