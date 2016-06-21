from django import forms


class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}), label="Add comment:")
    parent = forms.CharField(widget=forms.HiddenInput(), required=False)


