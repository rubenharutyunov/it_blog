from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group


class User(AbstractUser):
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(blank=True, null=True)
    favorite_posts = models.ManyToManyField('blog.Post', blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    objects = UserManager()    

    def __str__(self):
        return self.username


class Group(Group):
    pass