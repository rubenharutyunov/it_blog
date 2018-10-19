from django import template
from blog.models import Post

register = template.Library()


@register.inclusion_tag('to_moderate.html')
def get_moderation_sidebar():
    posts = Post.objects.filter(approved=False)
    count = posts.count()
    remaining = posts.count() - 50 if count > 50 else None
    return {
        'posts': posts[:50],
        'remaining': remaining,
        'count': count
    }
