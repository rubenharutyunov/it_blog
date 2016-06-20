from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest 
from blog.models import Post, Comment, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

types = {
    'most_viewed': 'Most Viewed',
    'new': 'New',
    'best': 'Best',
    'categories': 'Categories',
    'tags': 'Tags'
}


def pagination(request, obj, items):
    paginator = Paginator(obj, items)
    page = request.GET.get('page')
    try:
        obj = paginator.page(page)
    except PageNotAnInteger:
        obj = paginator.page(1)
    except EmptyPage:
        obj = paginator.page(paginator.num_pages)
    return obj


def get_posts(request, order_by='new'):
    if order_by == 'most_viewed':
        posts = Post.objects.order_by('-views')
    elif order_by == 'new':
        posts = Post.objects.order_by('-date_time')
    else:  # Best
        posts = Post.objects.order_by('-likes')
    posts = pagination(request, posts, 10)
    return render(request, 'posts.html', {
        'posts': posts,
        'type': order_by,
        'types': types
    })


def get_post(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'post.html', {
        'post': post,
    })


def get_categories_tags(request, type):
    if type == 'categories':
        result = Category.objects.all()
    else:  # Tags
        result = Tag.objects.all()
    result = pagination(request, result, 20)
    return render(request, 'categories_tags.html', {
        'result': result,
        'type': type,
        'types': types
    })


def placeholder(request, *args, **kwargs):
    return HttpResponse("placeholder")
