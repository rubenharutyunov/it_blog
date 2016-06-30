from django.conf.urls import url, include
from blog.views import placeholder, get_posts, get_post, posts_in_category, get_categories_tags, placeholder, like, add_to_fav, delete_comment, add_comment, refresh_comments, edit_comment, add_edit_post, delete_post

urlpatterns = [
    url(r'^$', get_posts, name='new_posts'),
    url(r'^viewed/', get_posts, {'order_by': 'most_viewed'}, name='most_viewed_posts'),
    url(r'^best/', get_posts, {'order_by': 'best'}, name='best_posts'),
    url(r'^post/(?P<slug>[\w-]+)/$', get_post, name='post'),
    url(r'^add/', add_edit_post, name='add_post'),
    url(r'^post/(?P<slug>[\w-]+)/edit/$', add_edit_post, name='edit_post'),
    url(r'^post/(?P<slug>[\w-]+)/delete/$', delete_post, name='delete_post'),
    url(r'^like/', like, name='like'),
    url(r'^fav/', add_to_fav, name='fav'),
    url(r'^del_comment/', delete_comment, name='del_comment'),
    url(r'^add_comment/', add_comment, name='add_comment'),
    url(r'^edit_comment/', edit_comment, name='edit_comment'),
    url(r'^refresh_comments/', refresh_comments, name='add_comment'),
    url(r'^categories/', get_categories_tags, {'type': 'categories'}, name='categories'),
    url(r'^tags/', get_categories_tags, {'type': 'tags'}, name='tags'),
    url(r'^category/(?P<slug>[\w-]+)/$', posts_in_category, {'type': 'category'}, name='category'),
    url(r'^tag/(?P<slug>[\w-]+)/$', posts_in_category, {'type': 'tag'}, name='tag'),
]