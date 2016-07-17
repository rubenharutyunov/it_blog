from django import forms
from django.utils.translation import ugettext as _
from navigation.models import BlogNavigationItem
from navigation.widgets import AwesomeFontWidget
from navigation.utils import get_icons


CHOICES = get_icons()
auth_choices = (
    (None, _("Not set")),
    (1, _("Authenticated")),
    (0, _("Not authenticated")),
    (2, _("Is Staff"))

)


class NavigationItemForm(forms.ModelForm):
    icon = forms.ChoiceField(required=False, choices=CHOICES, widget=AwesomeFontWidget(choices=CHOICES), label=_("Icon"))
    order = forms.IntegerField(widget=forms.HiddenInput)
    auth = forms.ChoiceField(required=False, choices=(auth_choices), label=_("Auth"),
                             help_text=_("If user need to be authenticated to see item"))

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
        fields = ('name', 'auth', 'page', 'custom_url', 'urls_name', 'icon', 'parent', 'order')

    def clean_custom_url(self):
        return self.cleaned_data['custom_url'] or None

