from django.db import models
from users.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    views = models.IntegerField(default=0)  
    likes = models.IntegerField(default=0) 
    date_time = models.DateTimeField(auto_now=True) 
    author = models.ForeignKey(User)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        get_latest_by = "-date_time"
        ordering = ['-date_time', 'title']

    def __str__(self):
        return self.title    

class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, editable=False)
    date_time = models.DateTimeField(auto_now=True) 
    likes = models.IntegerField(default=0)
    post = models.ForeignKey(Post, blank=True, null=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        get_latest_by = "date_time"
        ordering = ['-post', 'date_time']

    def __str__(self):
        return "User %s at %s" % (self.author, self.date_time)        