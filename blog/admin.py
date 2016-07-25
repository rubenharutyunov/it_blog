from django.contrib import admin
from blog.models import Post, Comment, Category, Tag, BlogFlatPage
from blog.forms import BlogFlatPageForm
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags
from django.db.models import TextField
from django.utils.translation import ugettext as _
from mptt.admin import MPTTModelAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Helper functions
def save_current_user(request, instance, form):
    user = request.user 
    instance = form.save(commit=False)
    if not hasattr(instance, 'author'):
        instance.author = user
    instance.save()
    form.save_m2m()
    return instance


def truncate_text(text):
    if len(text) < 100:
        return text
    return "%s..." % text[:100]


def show_urls(objects):
    res = ''
    for count, object_ in enumerate(objects):
        if object_:
            info = (object_._meta.app_label, object_._meta.model_name)
            admin_url = reverse('admin:%s_%s_change' % info, args=(object_.pk,))
            res += '<a href="%s">%s</a>%s ' % (admin_url,object_.title, ',' if count < len(objects)-1 else '')
        else:
            return None    
    return res or None
    

def approve_action(modeladmin, request, queryset):
    queryset.update(approved=True)
approve_action.short_description = _("Approve selected")


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('views',  'author')
    list_display = ('title', 'date_time', 'author', 'approved', 'views', 'post_likes', 'post_category')
    search_fields = ('title', 'text', 'author__username')
    list_filter = ('approved', 'author__username', 'category', 'tags')
    actions = [approve_action]

    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }

    def post_tags(self, obj):
        tags = obj.tags.all()
        return show_urls(tags)
    post_tags.short_description = _("Tags")
    post_tags.allow_tags = True

    def post_likes(self, obj):
        return len(obj.likes.all())
    post_likes.short_description = _("Likes")

    def post_category(self, obj):
        category = obj.category
        return show_urls([category])
    post_category.short_description = _("Category")
    post_category.allow_tags = True   

    def comment_count(self, obj):
        return obj.comment_set.count() 
    comment_count.short_description = _('Comments')

    def save_model(self, request, instance, form, change):
        return save_current_user(request, instance, form) 


class CommentAdmin(MPTTModelAdmin):
    list_display = ('post', 'author', 'date_time', 'truncate')
    readonly_fields = ('likes',)
    search_fields = ('text',)

    def truncate(self, obj):
        text = strip_tags(obj.text)
        return truncate_text(text)
    truncate.short_description = _('Text')

    def save_model(self, request, instance, form, change):
        return save_current_user(request, instance, form) 


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',  'truncate', 'post_count')

    def truncate(self, obj):
        text = strip_tags(obj.description)
        return truncate_text(text)
    truncate.short_description = _('Description')

    def post_count(self, obj):
        posts = Post.objects.filter(category=obj)
        return show_urls(posts)
    post_count.allow_tags = True    
    post_count.short_description = _('Posts in category')


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_count')

    def post_count(self, obj):
        posts = Post.objects.filter(tags=obj)
        return show_urls(posts)
    post_count.short_description = _('Posts with tag')
    post_count.allow_tags = True        


class BlogFlatPageAdmin(FlatPageAdmin):
    form = BlogFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
    )
    formfield_overrides = {
        TextField: {'widget': CKEditorUploadingWidget}
    }


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.unregister(FlatPage)
admin.site.register(BlogFlatPage, BlogFlatPageAdmin)

