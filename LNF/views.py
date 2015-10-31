from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic import View

from .models import Post

class LostPostView(View):
    model = Post

    def get(self, request):
        lost_post_list = Post.objects.filter(state='Lost')
        context = {'lost_post_list': lost_post_list}
        return render(request, 'posts/lostposts.html', context)
		
class FoundPostView(View):
    model = Post

    def get(self, request):
        found_post_list = Post.objects.filter(state='Found')
        context = {'found_post_list': found_post_list}
        return render(request, 'posts/foundposts.html', context)

