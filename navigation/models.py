from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey
from blog.models import Post, BlogFlatPage


class BlogNavigationItem(MPTTModel):
    menu_name = models.CharField(max_length=255, blank=True,
                                 help_text=_("Name to show in menu.\nUse [user] variable to display current user\nUse "
                                             "[search] variable to display search form"), verbose_name=_("Menu name"))
    post = models.ForeignKey(Post, blank=True, null=True, verbose_name=_("Post"))
    page = models.OneToOneField(BlogFlatPage, blank=True, null=True, verbose_name=_("Page"))
    custom_url = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Custom URL"))
    urls_name = models.CharField(blank=True, null=True, max_length=255, verbose_name=_("URL name"),
                                 help_text=_('Url name from urls.py files'))
    icon = models.CharField(blank=True, null=True, max_length=255, verbose_name=_("Icon"))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name=_("Parent"))
    order = models.PositiveIntegerField(default=0)
    auth = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Authentication"))
    nav = models.ForeignKey('BlogNavigation')

    class Meta:
        verbose_name = _("Menu Item")

    class MPTTMeta:
        order_insertion_by = ['order']

    def clean(self, *args, **kwargs):
        if (self.post and (self.page or self.custom_url or self.urls_name)) or (self.page and
           (self.post or self.custom_url or self.urls_name)) or (self.custom_url and
           (self.post or self.page or self.urls_name)) or (self.urls_name and
           (self.post or self.page or self.custom_url)):
            raise ValidationError(_("You should specify only one field"))
        if self.custom_url == "":
            self.custom_url = None
            print(self.custom_url)
        if self.urls_name == "":
            self.urls_name = None
        super(BlogNavigationItem, self).clean(*args, **kwargs)

    def get_url(self):
        if self.post:
            return reverse('post', kwargs={'slug': self.post.slug})
        elif self.page:
            return self.page.url
        elif self.urls_name:
            try:
                return reverse(self.urls_name)
            except NoReverseMatch:
                return ""
        elif self.custom_url:
            return self.custom_url
        else:
            return ""

    def get_item(self):
        return self.page or self.post or self.custom_url or self.urls_name

    def __str__(self):
        return "%s %s" % ("---" * self.get_level(), self.menu_name or _("Item with id %s" % self.id))


class BlogNavigation(models.Model):
    name = models.SlugField(unique=True)

    class Meta:
        verbose_name = _("Navigation Menu")
        verbose_name_plural = _("Navigation Menus")

    def __str__(self):
        return self.name.title()
