from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from LNF.forms import UserCreateForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
        ''' user is not logged in, show login form'''
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

		
