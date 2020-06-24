from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm

# LOGIN IMPORTS
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'user_app/index.html')


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required()
def special(request):
    return HttpResponse('You are logged in, Nice!')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save the user form to database
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            # update the hashed password
            user.save()

            # Now deal with extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)
            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                # if yes then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
                # Now save model
            profile.save()
            # Registration successful
            registered = True

        else:
            # if one of the form is invalid else get called
            print(user_form.errors, profile_form.errors)
    else:
        # Was not a HTTP Post so we render the forms as blank
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feedback
    # to the register.html page

    return render(request, 'user_app/register.html', {'user_form': user_form,
                                                      'profile_form': profile_form,
                                                      'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE!')
        else:
            print("Someone tried to login and failed!")
            print('username: {} and password {}'.format(username, password))
            return HttpResponse('Invalid login details supplied!')
    else:
        return render(request, 'user_app/login.html', {})
