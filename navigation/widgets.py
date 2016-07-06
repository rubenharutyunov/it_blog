from itertools import chain
from django import forms
from it_blog import settings
from django.utils.html import mark_safe, format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.datastructures import MultiValueDict

class AwesomeFontWidget(forms.Select):
    class Media:
        css = {
            'all': (
                "/static/navigation/css/awesome.css",
                "/static/navigation/select2/css/select2.min.css",
                "/static/font-awesome/css/font-awesome.min.css",
            )
        }
        js = (
            "/static/jquery-3.0.0.min.js",
            "/static/navigation/select2/js/select2.min.js",
            "/static/navigation/js/awesome.js",
        )

    def __init__(self, attrs=None, choices=()):
        super(AwesomeFontWidget, self).__init__(attrs=attrs, choices=choices)

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<option data-icon="{0}" value="{0}"{1}>{2}</option>',
                           option_value,
                           selected_html,
                           force_text(option_label),
                           )


