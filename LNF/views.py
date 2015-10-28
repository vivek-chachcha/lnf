from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
		
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')