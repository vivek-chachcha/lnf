from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from LNF.models import LNF_User
from LNF.forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def UserSignUp(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/profile/') #the user has already signed up, return to profile
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            user.save()
            lnf_user = LNF_User(user=user, name=form.cleaned_data['name']) 
            lnf_user.save()
            return HttpResponseRedirect('/profile/')
        else:
            return render_to_response('signup.html', {'form': form}, context_instance=RequestContext(request))

    else:
        # user has not signed up yet, show a form. 
        form = SignUpForm()
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
    return HttpResponseRedirect('/')


@login_required
def Profile(request):
    if not request.user.is_authenticated():
	    return HttpResponseRedirect('/login/')

    lnf_user= LNF_User.objects.filter(user=request.user)
    context = {'lnf_user': lnf_user}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

		