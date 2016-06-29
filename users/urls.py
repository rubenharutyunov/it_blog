from django.conf.urls import url, include
from users.views import sign_in, sign_out, get_users, get_user_posts, get_user_comments, get_user
from blog.views import placeholder

urlpatterns = [
    url(r'^users/', get_users, name='users'),
    url(r'^user/(?P<username>[\w-]+)/$', get_user, name='user'),
    url(r'^user/(?P<username>[\w-]+)/posts/', get_user_posts, name='user_posts'),
    url(r'^user/(?P<username>[\w-]+)/comments/', get_user_comments, name='user_posts'),
    url(r'^sign_in/', sign_in, name='sign_in'),
    url(r'^sign_out/', sign_out, name='sign_out'),
    url(r'^sign_up/', placeholder, name='sign_up'),
]