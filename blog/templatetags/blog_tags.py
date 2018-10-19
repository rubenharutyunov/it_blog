from django import template
from django.forms import CheckboxInput
from users.widgets import FileInputPreview
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


@register.filter(name='add_class')
def add_class(field, classname):
    return field.as_widget(attrs={'class': classname})


@register.filter(name='need_form_control')
def need_form_control(field):
    name = field.field.widget.__class__.__name__
    return not (name == CheckboxInput().__class__.__name__ or
                name == FileInputPreview().__class__.__name__)


@register.filter(name='approved_count')
def approved_count(user):
    return user.post_set.filter(approved=True).count()
