from django import template
register = template.Library()


@register.filter(name='get')
def get(dict, key):
    return dict.get(key) or ''


@register.filter(name='liked')
def liked(user, post):
    if post.likes.filter(id=user.id):
        return 'liked'
    return ''


@register.filter(name='fav')
def liked(user, post):
    if user.is_authenticated():
        if user.favorite_posts.filter(id=post):
            return 'fav'
    return ''
