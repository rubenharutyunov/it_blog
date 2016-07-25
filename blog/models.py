import itertools
from django.db import models
from django.utils.text import slugify
from transliterate import slugify as trans_slugify
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from users.models import User
from blog.utils import send_approved_email


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    text = models.TextField(verbose_name=_('Content'))
    excerpt = models.TextField(verbose_name=(_('Excerpt')), blank=True, null=True)
    slug = models.SlugField(unique=True, verbose_name=_('Slug'), blank=True)
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    likes = models.ManyToManyField(User, related_name='likes', blank=True, verbose_name=_('Likes'))
    date_time = models.DateTimeField(verbose_name=_('Date/Time'))
    author = models.ForeignKey(User, verbose_name=_('Author'))
    category = models.ForeignKey('blog.Category', blank=True, null=True, verbose_name=_('Category'))
    tags = models.ManyToManyField('blog.Tag', blank=True, verbose_name=_('Tags'))
    approved = models.BooleanField(default=True, verbose_name=_('Approved'))

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        get_latest_by = "-date_time"
        ordering = ['-date_time', 'title']

    def save(self, **kwargs):
        if self.pk is not None:
            orig = Post.objects.get(pk=self.pk)
            if not orig.approved and self.approved:
                send_approved_email(self)
        else:
            self.slug = orig = trans_slugify(self.title) or slugify(self.title)
            for x in itertools.count(1):
                if not Post.objects.filter(slug=self.slug).exists():
                    break
                self.slug = '%s-%d' % (orig, x)
        super(Post, self).save()

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    text = models.TextField(max_length=255, verbose_name=_('Content'))
    author = models.ForeignKey(User, editable=False, verbose_name=_('Author'))
    date_time = models.DateTimeField(auto_now=True, verbose_name=_('Date/Time'))
    likes = models.IntegerField(default=0, verbose_name=_('Likes'))
    post = models.ForeignKey(Post, verbose_name=_('Post'))
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name=_('Parent'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        get_latest_by = "date_time"
        ordering = ['-post', 'date_time']

    class MPTTMeta:
        order_insertion_by = ['-date_time']

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.post.slug})

    def __str__(self):
        return "User %s at %s" % (self.author, self.post)     


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    description = RichTextField(verbose_name=_('Description'))
    slug = models.SlugField(unique=True, null=True, verbose_name=_('Slug'))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse('categories')

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(unique=True, null=True, verbose_name=_('Slug'))

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def get_absolute_url(self):
        return reverse('tags')

    def __str__(self):
        return self.title


class BlogFlatPage(FlatPage):
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
