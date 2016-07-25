from django import forms
from blog.models import Post, BlogFlatPage
from django.contrib.flatpages.admin import FlatpageForm
from django.utils.translation import ugettext as _
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), label=_("Add comment:"))
    parent = forms.CharField(widget=forms.HiddenInput(), required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'excerpt', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Title')}),
            'text': CKEditorWidget(config_name='minimal'),
            'excerpt': CKEditorWidget(config_name='minimal'),
        }


class BlogFlatPageForm(FlatpageForm):
    class Meta:
        model = BlogFlatPage
        fields = ('url', 'title', 'content', 'sites')
