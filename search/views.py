from django.shortcuts import render
from haystack.views import SearchView


class OneModelSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        super(OneModelSearchView, self).__init__(*args, **kwargs)

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET
            if 'models' not in self.request.GET:
                data = {
                    'q': data['q'],
                    'models': 'blog.post'
                }

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)
