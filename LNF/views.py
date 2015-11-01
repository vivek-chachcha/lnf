from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext, loader
from LNF.forms import UserCreateForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from .models import Post
from .forms import PostForm
from PIL import Image
import json
import urllib.parse
import urllib.request


def UserSignUp(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') #the user has already signed up, return to profile
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(first_name = form.cleaned_data['firstname'], last_name = form.cleaned_data['lastname'], username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
            user.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))
    else:
        # user has not signed up yet, show a form. 
        form = UserCreateForm()
        context = {'form': form}
        return render_to_response('signup.html', context, context_instance=RequestContext(request))
				
def LoginRequest(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            lnf_user = authenticate(username=username, password=password)
            if lnf_user is not None:
                login(request, lnf_user)
                return HttpResponseRedirect('/profile/')
            else:
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
    else:
        """ user is not logged in, show login form"""
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))
	
def LogoutRequest(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def Profile(request):
    if not request.user.is_authenticated():
	    return HttpResponseRedirect('/login/')

    lnf_user= User.objects.get(username=request.user.username)
    context = {'lnf_user': lnf_user}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

		
def posts(request):
    all_post_list = Post.objects.order_by('-date_created')[:]
    context = {'all_post_list': all_post_list}
    return render(request, 'lnf/listView.html', context)
    
def createpost(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_post = form.save(commit=False)
	
            address_input = request.POST.get('address')
            address = urllib.parse.quote_plus(address_input)
            maps_api_url = "https://maps.google.com/maps/api/geocode/json?address=%s&key=%s" % (address, "AIzaSyAHjZ8463T8-5IvzglxU4TtWx3tMxsnxnc")
            response = urllib.request.urlopen(maps_api_url)
            data = json.loads(response.read().decode('utf8'))
            if data['status'] == 'OK':
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                new_post.lat = float(lat)
                new_post.long = float(lng)
                new_post.save()
            else:
                # DO ERROR HANDLING
                return HttpResponseRedirect('error')      
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('posts'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()

    return render(request, 'lnf/createpost.html', {'form': form})
    
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'lnf/detail.html', {'post': post})
    
def error(request):
    return render(request, 'lnf/error.html')
