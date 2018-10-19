import datetime
from haystack import indexes
from blog.models import BlogFlatPage, Post, Category, Tag, Comment


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date_time__lte=datetime.datetime.now())


class BlogFlatPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BlogFlatPage


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Category


class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Tag


class CommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr="text")

    def get_model(self):
        return Comment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(date_time__lte=datetime.datetime.now())