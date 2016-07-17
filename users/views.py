from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext as _
from users.forms import SignInForm, SignUpForm, ProfileEditForm
from users.models import User
from users.utils import generate_activation_key, send_activation_email, TOMORROW
from blog.views import pagination


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
                    next = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
                    return HttpResponseRedirect(next)
                else:
                    form.add_error(None, _('User is not active'))
            else:
                form.add_error(None, _('Username or password are incorrect'))

    return render(request, 'sign_in.html', {
        'form': form
    })


def sign_up(request, edit=False):
    if request.method == 'GET':
        if edit and request.user.is_authenticated():
            form = ProfileEditForm(instance=request.user)
        else:
            form = SignUpForm()
    else:
        if edit and request.user.is_authenticated():
            form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, request.user)
                return HttpResponseRedirect('/')
        else:
            form = SignUpForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return render(request, 'registration_success.html', {
                    'username': form.cleaned_data['username']
                })
    return render(request, 'sign_up.html', {
        'form': form
    })


def activate_account(request, activation_key):
    user = get_object_or_404(User, activation_key=activation_key)
    expired = False
    already_activated = False
    if not user.is_active:
        if timezone.now() > user.key_expires:
            expired = True
        else:
            user.is_active = True
            user.save()
    else:
        already_activated = True
    return render(request, 'activation.html', {
        'user': user,
        'expired': expired,
        'already_activated': already_activated
    })


def new_activation_link(request, username):
    user = get_object_or_404(User, username=username)
    if user is not None and not request.user.is_authenticated() and not user.is_active:
        activation_key = generate_activation_key(username)
        user.activation_key = activation_key
        user.key_expires = TOMORROW
        user.save()
        send_activation_email(username, activation_key, user.email)
        return render(request, 'new_activation_link.html')
    else:
        raise PermissionDenied


def sign_out(request):
    user = request.user
    if user.is_authenticated():
        logout(request)
    return HttpResponseRedirect('/')


def get_users(request):
    users = User.objects.all()
    users = pagination(request, users, 20)
    return render(request, 'users.html', {
        'users': users
    })


def get_user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = pagination(request, user.post_set.filter(approved=True), 10)
    return render(request, 'posts.html', {
        'posts': posts,
        'additional': "%s's posts" % username
    })


def get_user_comments(request, username=None):
    user = get_object_or_404(User, username=username)
    comments = pagination(request, user.comment_set.all(), 20)
    return render(request, 'user_comments.html', {
        'comments': comments,
        'username': user.username
    })


def get_user(request, username=None):
    editable = False
    username = username or request.user.username
    if request.user.username == username:
        editable = True
    user = get_object_or_404(User, username=username)
    return render(request, 'user.html', {
        'user': user,
        'editable': editable
    })