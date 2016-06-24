from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from blog.models import Post, Comment, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import http
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from blog.forms import CommentForm
import json


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
        'type': order_by
    })


def get_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_id = request.POST.get('parent')
            text = request.POST.get('text')
            if parent_id:
                parent = get_object_or_404(Comment, id=int(parent_id))
                comment = Comment(post=post, text=text, author=request.user, parent=parent)
            else:
                comment = Comment(post=post, text=text, author=request.user,)
            comment.save()
            return http.HttpResponseRedirect(request.path)
    else:
        comment_form = CommentForm()
    response = render(request, 'post.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })
    cookie_name = 'viewed_%s' % post.id
    if cookie_name not in request.COOKIES:
        response.set_cookie(cookie_name, '1', 18000)
        Post.objects.filter(slug=slug).update(views=F('views') + 1)
    return response


def get_categories_tags(request, type):
    if type == 'categories':
        result = Category.objects.all()
    else:  # Tags
        result = Tag.objects.all()
    result = pagination(request, result, 20)
    return render(request, 'categories_tags.html', {
        'result': result,
        'type': type
    })


def posts_in_category(request, slug, type):
    if type == "category":
        category = get_object_or_404(Category, slug=slug)
        posts = category.post_set.all()
        title = category.title
    else:  # Tag
        tag = get_object_or_404(Tag, slug=slug)
        posts = tag.post_set.all()
        title = tag.title
    posts = pagination(request, posts, 10)
    return render(request, 'posts.html', {
        'posts': posts,
        'type': '',
        'additional': title
    })


@require_POST
def like(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated():
        if not post.likes.filter(id=request.user.id):
            status = 'LIKED'
            post.likes.add(request.user)
        else:
            status = 'UNLIKED'
            post.likes.remove(request.user)
    else:
        status = 'AUTH_REQUIRED'
    res = {'status': status, 'likes': post.likes.count()}
    return HttpResponse(json.dumps(res), content_type='application/json')


@require_POST
def add_to_fav(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if request.user.is_authenticated():
        if not user.favorite_posts.filter(id=post_id):
            status = 'ADDED'
            user.favorite_posts.add(post)
        else:
            status = 'REMOVED'
            user.favorite_posts.remove(post)
    else:
        status = 'AUTH_REQUIRED'
    res = {'status': status, 'count': post.favorite.count()}
    return HttpResponse(json.dumps(res), content_type='application/json')


@require_POST
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    get_object_or_404(Comment, id=comment_id).delete()
    return HttpResponse(json.dumps({'status': 'OK'}))


@require_POST
def add_comment(request):
    post_id = request.POST.get('post_id')
    comment_text = request.POST.get('text')
    comment_author = request.user
    comment_parent = request.POST.get('parent')
    post = get_object_or_404(Post, id=post_id)
    if comment_parent:  # If have parents (is reply)
        comment = Comment.objects.create(text=comment_text, author=comment_author, post=post, parent_id=comment_parent)
        comments = get_object_or_404(Comment, id=comment_parent).get_descendants()  # Get all descendants in tree
    else:
        comment = Comment.objects.create(text=comment_text, author=comment_author, post=post)
        comments = [comment]  # Single comment
    res_html = render_to_string('comment.html', {
        'comments': comments,
    }, request=request)
    return HttpResponse(json.dumps({'status': 'OK', 'comment_id': comment.id, 'html': res_html}))


def placeholder(request, *args, **kwargs):
    return HttpResponse("placeholder")