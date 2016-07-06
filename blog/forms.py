from django import forms
from blog.models import Post, BlogFlatPage
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.admin import FlatpageForm


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), label="Add comment:")
    parent = forms.CharField(widget=forms.HiddenInput(), required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'tags']
        widgets = {
            'Title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'Text': CKEditorWidget(attrs={'rows': 500, 'cols': 10}),
        }


class BlogFlatPageForm(FlatpageForm):
    class Meta:
        model = BlogFlatPage
        fields = ('url', 'title', 'content', 'sites', 'name')
