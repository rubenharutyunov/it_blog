from django.contrib import admin
from blog.models import Post, Comment  
from django.utils.html import strip_tags

def save_current_user(request, instance, form):
    user = request.user 
    instance = form.save(commit=False)
    instance.author = user
    instance.save()
    form.save_m2m()
    return instance

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('views', 'likes', 'author')
    list_display = ('title', 'date_time', 'author', 'views', 'comment_count')
    search_fields = ('title', 'text', 'author__username')

    def comment_count(self, obj):
        return obj.comment_set.count() 
    comment_count.short_description = 'Comments'   

    def save_model(self, request, instance, form, change):
        return save_current_user(request, instance, form) 

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date_time', 'truncate')
    readonly_fields = ('likes',)
    search_fields = ('text',)

    def truncate(self, obj):
        text = strip_tags(obj.text)
        if len(text) < 100:
            return text
        return "%s..." % obj.text[:100]
    truncate.short_description = 'Text'    

    def save_model(self, request, instance, form, change):
        return save_current_user(request, instance, form) 
        
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)