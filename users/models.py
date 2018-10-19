from urllib.parse import urlsplit
from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import AbstractUser, UserManager, Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields import RichTextUploadingField


@deconstructible
class URLDomainValidator(object):
    def __init__(self, domain_list):
        self.domain_list = domain_list

    def __call__(self, url):
        for domain in self.domain_list:
            if domain in "{0.netloc}".format(urlsplit(url)):
                return url
        raise ValidationError(_("Enter a valid URL."))

    def __eq__(self, other):
        return self.domain_list == other.domain_list


class User(AbstractUser):
    rating = models.IntegerField(default=0, verbose_name=_("Rating"))
    avatar = models.ImageField(blank=True, null=True, verbose_name=_("Avatar"))
    favorite_posts = models.ManyToManyField('blog.Post', blank=True, related_name='favorite',
                                            verbose_name=_("Favorite Posts"))
    personal_info = RichTextUploadingField(blank=True, verbose_name=_("Personal Info"))
    website = models.URLField(blank=True, verbose_name=_("Website"))
    facebook = models.URLField(blank=True, validators=[URLDomainValidator(['fb.com', 'facebook.com'])])
    gplus = models.URLField(blank=True, verbose_name="Google Plus", validators=[URLDomainValidator(['plus.google.com'])])
    twitter = models.URLField(blank=True, validators=[URLDomainValidator(['twitter.com'])])
    github = models.URLField(blank=True, validators=[URLDomainValidator(['github.com'])])
    linkedin = models.URLField(blank=True, validators=[URLDomainValidator(['linkedin.com'])])
    vk = models.URLField(blank=True, validators=[URLDomainValidator(['vk.com', 'vkontakte.ru'])])
    activation_key = models.CharField(max_length=40, blank=True, null=True)
    key_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    objects = UserManager()    

    def __str__(self):
        return self.username


class Group(Group):
    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
