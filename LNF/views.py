from django.shortcuts import get_object_or_404, render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Post
from .forms import PostForm
from PIL import Image
import json
import urllib.parse
import urllib.request

def posts(request):
    all_post_list = Post.objects.order_by('-date_created')[:]
    context = {'all_post_list': all_post_list}
    return render(request, 'lnf/listView.html', context)
    
def createpost(request):
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
