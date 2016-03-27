from django.conf.urls import url, include
from blog.views import placeholder, get_posts

urlpatterns = [
    url(r'^$', get_posts, name='posts_index'),
    url(r'^all/', get_posts, {'order_by' : 'newest'}, name='newest_posts'),
    url(r'^best/', get_posts, {'order_by' : 'best'}, name='best_posts'),
] 