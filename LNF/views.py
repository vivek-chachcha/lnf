from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext, loader
from LNF.forms import UserCreateForm, LoginForm,BookmarkForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Post, BookmarkedPostList, BookmarkedPost
from .forms import PostForm
from PIL import Image
import json
import urllib.parse
import urllib.request
from urllib.request import urlopen

def importData(request):
    url = "ftp://webftp.vancouver.ca/OpenData/json/LostAnimals.json"
    data = urlopen(url).read().decode('utf-8')
    data = json.loads(data)

    for entry in data:
        m = Post(date = entry['Date'], colour = entry['Color'], breed = entry['Breed'], name = entry['Name'], date_created = entry[
'DateCreated'])
        m.sex = entry['Sex'] if entry['Sex'] else 'X'
        m.state = 0 if entry['State'] == 'Lost' else 1
        m.save()

    return HttpResponseRedirect('/profile/')


def signUpUser(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') #the user has already signed up, return to profile
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(first_name = form.cleaned_data['firstname'], last_name = form.cleaned_data['lastname'], 
username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
            user.save()
            bmList = BookmarkedPostList(user=user)
            bmList.save(user)
            return HttpResponseRedirect('/profile/')
        else:
            return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))
    else:
        # user has not signed up yet, show a form. 
        form = UserCreateForm()
        context = {'form': form}
        return render_to_response('signup.html', context, context_instance=RequestContext(request))
                
def loginUser(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            lnf_user = authenticate(username=username, password=password)
            if lnf_user is not None:
                login(request, lnf_user)
                return HttpResponseRedirect('/')
            else:
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
    else:
        """ user is not logged in, show login form"""
        form = LoginForm()
        context = {'form': form}
        return render_to_response('login.html', context, context_instance=RequestContext(request))
    
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def getProfile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')

    lnf_user= User.objects.get(username=request.user.username)
    context = {'lnf_user': lnf_user}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

    
def createpost(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.save(request.POST.get('address'))
            return HttpResponseRedirect('/%d/post/' % new_post.id)
    else:
        form = PostForm()

    return render(request, 'createpost.html', {'form': form})
    
def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':    
    
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
            
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bml = BookmarkedPostList.objects.get(user=request.user)
            bmp = BookmarkedPost.objects.filter(bmList=bml,post=Post.objects.get(id=post_id))
            if bmp.exists():
                bmp = BookmarkedPost.objects.get(bmList=bml,post=Post.objects.get(id=post_id))
                bml.bmList.remove(bmp)
                bmp.delete()
            isBookmarked = form.cleaned_data['bookmark']        
            if isBookmarked:
                newBmPost = BookmarkedPost(post=Post.objects.get(id=post_id),bmList=bml)
                newBmPost.save()
                bml.bmList.add(newBmPost)
            
            return HttpResponseRedirect('/%s/post/' % post_id)
    else:
        form = BookmarkForm()

    return render(request, 'detail.html', {'post': post, 'form':form})
    
def error(request):
    return render(request, 'error.html')

def posts(request):
    # default all post list
    all_post_list = Post.objects.order_by('-date_created')[:]
    
    # reset all post list if request is to reset filters
    if (request.GET.get('reset')):
        all_post_list = Post.objects.order_by('-date_created')[:]
        
    # handle filter functionality
    if (request.GET.get('filter')):
        name_crit = request.GET.get('name')
        if (name_crit != ""):
            all_post_list = all_post_list.filter(name__icontains=name_crit)

        date_start = request.GET.get('date1')
        date_end = request.GET.get('date2')
        if (date_start != ""):
            if (date_end != ""):
                all_post_list = all_post_list.filter(date__range=[date_start, date_end])
            else:
                all_post_list = all_post_list.filter(date=date_start)

        colour_crit = request.GET.get('colour')
        if (colour_crit != ""):
            all_post_list = all_post_list.filter(colour__icontains=colour_crit)
        
        breed_crit = request.GET.get('breed')
        if (breed_crit != ""):
            all_post_list = all_post_list.filter(breed__icontains=breed_crit)

        sex_crit = request.GET.get('sex')
        if (sex_crit != ""):
            all_post_list = all_post_list.filter(sex=sex_crit)
    
    # handle sorting functionality based on current filtered set of posts
    if (request.GET.get('sort-')):
        sort_criteria = request.GET.get('sort-').lower()
        current_posts = request.GET.get('list')
        split_posts = current_posts.split(",")
        ids = [post[8:9] for post in split_posts]
        ids_int = [int(id) for id in ids]
        filtered_posts = Post.objects.filter(pk__in=ids)
        all_post_list = filtered_posts.order_by(sort_criteria)
    elif (request.GET.get('sort+')):
        sort_criteria = request.GET.get('sort+').lower()
        current_posts = request.GET.get('list')
        split_posts = current_posts.split(",")
        ids = [post[8:9] for post in split_posts]
        ids_int = [int(id) for id in ids]
        filtered_posts = Post.objects.filter(pk__in=ids)
        all_post_list = filtered_posts.order_by("-" + sort_criteria)

    # filter one more time based on lost/found state and return correct html page
    if 'found' in request.get_full_path():
        found_post_list = all_post_list.filter(state=1)
        context = {'found_post_list': found_post_list}

        if 'map' in request.get_full_path():
            return render(request, 'posts/foundpostsmap.html', context)
        else:
            return render(request, 'posts/foundpostslist.html', context)
    else:
        lost_post_list = all_post_list.filter(state=0)
        context = {'lost_post_list': lost_post_list}

        if 'map' in request.get_full_path():
            return render(request, 'posts/lostpostsmap.html', context)
        else:
            return render(request, 'posts/lostpostslist.html', context)

def displayBookmarkedPosts(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    bm_post_list = BookmarkedPostList.objects.get(user=request.user).bmList.all().order_by('-date_bmed')[:]
    all_post_list = [bookmarkedpost.post for bookmarkedpost in bm_post_list]
    context = {'title': 'Bookmarked Posts', 'all_post_list': all_post_list}
    return render(request, 'listView.html', context)
    
def HomeView(request):
    return render(request, 'home.html')
        
def AboutView(request):
    return render(request, 'about.html')