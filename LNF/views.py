from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic import View

from .models import Post

class PostView(View):
    model = Post
    template_name = 'posts/posts.html'

    def get(self, request):
        post_list = Post.objects.all()
        context = {'post_list': post_list}
        return render(request, 'posts/posts.html', context)
