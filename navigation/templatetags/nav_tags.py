import importlib
from django import template
from django.conf import settings
from django.db.models import Q
from navigation.models import BlogNavigation, BlogNavigationItem


register = template.Library()


@register.inclusion_tag('navigation.html')
def get_nav(name, request):
    try:
        navigation = BlogNavigation.objects.get(name=name)
    except BlogNavigation.DoesNotExist:
        return None
    nav_items = navigation.blognavigationitem_set.all()
    menu_classes = None
    if getattr(settings, 'NAV_CLASSES', None):
        menu_classes = settings.NAV_CLASSES.get(name)
    search_form = getattr(settings, 'NAV_SEARCH_FORM', None)
    if search_form:
        splited = search_form.split('.')
        name = splited[-1]
        module = '.'.join(splited[:-1])
        search_form = importlib.import_module(module)
        search_form = getattr(search_form, name)

    return {
        'items': nav_items,
        'request': request,
        'attrs': menu_classes,
        'search_form': search_form()
    }


@register.simple_tag()
def get_active(node, path):
    """
    Returns 'active' or 'active_sub'
    If one of children is active parent become active too
    """
    if path == node.get_url():
        if node.parent:
            return "active_sub"
        else:
            return "active"
    if node.children:  # Make active if one of children is active
        for child in node.get_children():
            if child.get_url() == path and node.parent:  # Have parent
                return 'active_sub'
            elif child.get_url() == path and not node.parent:  # Root
                return 'active'


@register.filter(name='show_user')
def show_user(val, request):
    if '[user]' in val:
        val = val.replace('[user]', request.user.username)
    return val


@register.filter(name='is_search')
def is_search(val):
    if val and '[search]' in val:
        return True
    return False


@register.filter(name='check_perms')
def check_perms(auth, user):
    """
    Checks permissions to show item.
    Returns True or False
    """
    if not auth:
        return True
    if user.is_authenticated() and auth == "1":
        return True
    elif user.is_staff and auth == "2":
         return True
    elif not user.is_authenticated() and auth == "0":
        return True
    return False

