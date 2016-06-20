from django.conf.urls import url, include
from blog.views import placeholder, get_posts, get_post, types, get_categories_tags

urlpatterns = [
    url(r'^$', get_posts, name='new_posts'),
    url(r'^all/', get_posts, {'order_by': 'most_viewed'}, name='most_viewed_posts'),
    url(r'^best/', get_posts, {'order_by': 'best'}, name='best_posts'),
    url(r'^post/(?P<slug>[\w-]+)/$', get_post, name='post'),
    url(r'^user/(?P<username>[\w-]+)/$', placeholder, name='user'),
    url(r'^categories/', get_categories_tags, {'type': 'categories'}, name='categories'),
    url(r'^tags/', get_categories_tags, {'type': 'tags'}, name='tags'),
    url(r'^category/(?P<name>[\w-]+)/$', placeholder, {'type': 'categories'}, name='category'),
    url(r'^tag/(?P<name>[\w-]+)/$', placeholder, name='tag'),
]