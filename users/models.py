from urllib.parse import urlsplit
from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingField


@deconstructible
class URLDomainValidator(object):
    def __init__(self, domain_list):
        self.domain_list = domain_list

    def __call__(self, url):
        for domain in self.domain_list:
            if domain in "{0.netloc}".format(urlsplit(url)):
                return url
        raise ValidationError("Enter a valid URL.")

    def __eq__(self, other):
        return self.domain_list == other.domain_list


class User(AbstractUser):
    rating = models.IntegerField(default=0)
    avatar = models.ImageField(blank=True, null=True)
    about = RichTextUploadingField(blank=True)
    favorite_posts = models.ManyToManyField('blog.Post', blank=True, related_name='favorite')
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True, validators=[URLDomainValidator(['fb.com', 'facebook.com'])])
    gplus = models.URLField(blank=True, verbose_name="Google Plus", validators=[URLDomainValidator(['plus.google.com'])])
    twitter = models.URLField(blank=True, validators=[URLDomainValidator(['twitter.com'])])
    github = models.URLField(blank=True, validators=[URLDomainValidator(['github.com'])])
    linkedin = models.URLField(blank=True, validators=[URLDomainValidator(['linkedin.com'])])
    vk = models.URLField(blank=True, validators=[URLDomainValidator(['vk.com', 'vkontakte.ru'])])

    def links(self):
        return [self[name] for name in filter(lambda x: x.endswith('_url'), self.fields.values())]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
    objects = UserManager()    

    def __str__(self):
        return self.username


class Group(Group):
    pass