from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from users.forms import SignInForm
from users.models import User

def sign_in(request):
    if request.method == 'GET':
        form = SignInForm()
    else:
        form = SignInForm(request.POST)
        if form.is_valid():
            username_or_email = form.data.get('username_or_email')
            password = form.data.get('password')
            user = authenticate(username=username_or_email, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if 'remember' in request.POST:
                        request.session.set_expiry(1209600)  # 2 weeks
                    return HttpResponseRedirect('/')
                else:
                    form.add_error(None, 'User is blocked')
            else:
                form.add_error(None, 'Username or password are incorrect')

    return render(request, 'sign_in.html', {
        'form': form
    })


def sign_out(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')


def get_users(request):
    users = User.objects.all()
    return render(request, 'users.html', {
        'users': users
    })