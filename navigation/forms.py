from django import forms
from navigation.models import BlogNavigationItem, BlogNavigation
from navigation.widgets import AwesomeFontWidget
from navigation.utils import get_icons
from django.core.cache import cache


CHOICES = get_icons()
auth_choices = (
    (None, "Not set"),
    (1, "Authenticated"),
    (0, "Not authenticated"),
    (2, "Is Staff")
)


class NavigationItemForm(forms.ModelForm):
    icon = forms.ChoiceField(required=False, choices=CHOICES, widget=AwesomeFontWidget(choices=CHOICES), label="Icon")
    order = forms.IntegerField(widget=forms.HiddenInput)
    auth = forms.ChoiceField(required=False, choices=(auth_choices), label="Auth",
                             help_text="If user need to be authenticated to see item")

    class Media:
        js = (
            '/static/navigation/js/inline-ordering.js',
        )
        css = {
            'all': (
                '/static/navigation/css/tabular-inline.css',
            )
        }

    class Meta:
        model = BlogNavigationItem
        fields = ('menu_name', 'auth', 'page', 'custom_url', 'urls_name', 'icon', 'parent', 'order')

    def clean_custom_url(self):
        return self.cleaned_data['custom_url'] or None
