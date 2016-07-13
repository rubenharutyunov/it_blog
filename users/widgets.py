from django.forms.widgets import FileInput
from django.template.loader import render_to_string


class FileInputPreview(FileInput):
    class Media:
        js = (
            '/static/blog/js/upload_field.js',
        )
        css = {
            'all': (
                '/static/blog/css/upload_field.css',
            )
        }

    def render(self, name, value, attrs=None):
        return render_to_string('file_input_preview.html', {
            'input': super(FileInput, self).render(name, None, attrs=attrs)
        })
