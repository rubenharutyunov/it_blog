from django import template
from django.db.models import Count
from blog.models import Post, Category, Tag

register = template.Library()


@register.inclusion_tag('sidebar.html')
def get_sidebar():
    new = Post.objects.order_by('-date_time')[:10]
    best = Post.objects.order_by('-likes')[:10]
    top_categories = Category.objects.annotate(num_items=Count('post__category')).order_by('-num_items')[:10]
    top_tags = Tag.objects.annotate(num_items=Count('post__tags')).order_by('-num_items')[:10]
    return {
        'new': new,
        'best': best,
        'top_categories': top_categories,
        'top_tags': top_tags
    }