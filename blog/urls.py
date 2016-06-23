from django.conf.urls import url, include
from blog.views import placeholder, get_posts, get_post, posts_in_category, get_categories_tags, placeholder, like, add_to_fav

urlpatterns = [
    url(r'^$', get_posts, name='new_posts'),
    url(r'^viewed/', get_posts, {'order_by': 'most_viewed'}, name='most_viewed_posts'),
    url(r'^best/', get_posts, {'order_by': 'best'}, name='best_posts'),
    url(r'^post/(?P<slug>[\w-]+)/$', get_post, name='post'),
    url(r'^add/', placeholder, name='add_post'),
    url(r'^like/', like, name='like'),
    url(r'^fav/', add_to_fav, name='fav'),
    url(r'^categories/', get_categories_tags, {'type': 'categories'}, name='categories'),
    url(r'^tags/', get_categories_tags, {'type': 'tags'}, name='tags'),
    url(r'^category/(?P<slug>[\w-]+)/$', posts_in_category, {'type': 'category'}, name='category'),
    url(r'^tag/(?P<slug>[\w-]+)/$', posts_in_category, {'type': 'tag'}, name='tag'),
]