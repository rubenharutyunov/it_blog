from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest 
from blog.models import Post, Comment

def get_posts(request, order_by='most_viwed'):
    if order_by == 'most_viwed':
        posts = Post.objects.order_by('-views')
    elif order_by == 'newest':
        posts = Post.objects.order_by('-date_time')
    elif order_by == 'best':
        posts = Post.objects.order_by('-likes')    
    # TODO: Replace with templates    
    res = ''
    for post in posts: 
        res += "%s %s <br>" % (post.title, post.date_time)
    return HttpResponse(res)    


def placeholder(request):
    return HttpResponse("placeholder")
