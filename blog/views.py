import json
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import http
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from blog.forms import CommentForm, PostForm
from blog.models import Post, Comment, Category, Tag
from blog.utils import clean_untrusted_tags


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
        posts = Post.objects.filter(approved=True).order_by('-views')
        type = _("Most Viewed")
    elif order_by == 'new':
        posts = Post.objects.filter(approved=True).order_by('-date_time')
        type = _("New")
    else:  # Best
        posts = Post.objects.filter(approved=True).order_by('-likes')
        type = _("Best")
    posts = pagination(request, posts, 10)
    return render(request, 'posts.html', {
        'posts': posts,
        'type': type
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
        type = _('Categories')
        tags = False
    else:  # Tags
        result = Tag.objects.all()
        type = _('Tags')
        tags = True
    result = pagination(request, result, 20)
    return render(request, 'categories_tags.html', {
        'result': result,
        'type': type,
        'tags': tags
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


@login_required
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


@login_required
@require_POST
def delete_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
        return HttpResponse(json.dumps({'status': 'OK', 'count': Comment.objects.filter(post=comment.post).count()}))
    raise PermissionDenied


@login_required
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
    res_html = render_to_string('comments.html', {
        'comments': comments,
    }, request=request)
    return HttpResponse(json.dumps({'status': 'OK', 'comment_id': comment.id, 'html': res_html}))


@require_POST
def refresh_comments(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    comments = post.comment_set.all()
    return HttpResponse(render_to_string('comments.html', {
        'comments': comments,
    }, request=request))


@login_required
@require_POST
def edit_comment(request):
    comment_text = request.POST.get('text')
    comment_id = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user or request.user.is_staff:
        comment.text = comment_text
        comment.save()
        descendants = comment.get_descendants()
        replies = render_to_string('comments.html', {
            'comments': descendants
        }, request=request)
        return HttpResponse(json.dumps({'status': 'OK', 'comment_id': comment_id, 'replies': replies}))
    raise PermissionDenied


@login_required
def add_edit_post(request, slug=None):
    if request.method == 'GET':
        form = PostForm()
        if slug:  # If editing
            post = get_object_or_404(Post, slug=slug)
            if request.user.is_staff or request.user == post.author:
                form = PostForm(instance=post)
            else:
                raise PermissionDenied
    else:  # POST
        if not slug:
            form = PostForm(request.POST)
        else:
            form = PostForm(request.POST, instance=get_object_or_404(Post, slug=slug))
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            if not request.user.is_staff:
                instance.approved = False
            instance.text = clean_untrusted_tags(instance.text)
            instance.save()
            form.save_m2m()
            return render(request, 'add_post_success.html', {})
    return render(request, 'add_edit_post.html', {
        'form': form,
        'edit': slug is not None
    })


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_staff or request.user == post.author:
        post.delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect(reverse('new_posts'))