from django.conf.urls import url, include
from blog.views import placeholder

urlpatterns = [
    url(r'^users/', placeholder, name='users'),
    url(r'^user/(?P<username>[\w-]+)/$', placeholder, name='user'),
    url(r'^profile/', placeholder, name='profile'),
    url(r'^sign_in/', placeholder, name='sign_in'),
    url(r'^sign_up/', placeholder, name='sign_up'),
]