from django import forms
from haystack.forms import ModelSearchForm, haystack_get_model, model_choices


class OneModelSearchForm(ModelSearchForm):
    def __init__(self, *args, **kwargs):
        super(OneModelSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = forms.ChoiceField(initial='blog.post', choices=model_choices(), required=False, label='Search In',)

    def get_models(self):
        """Return a list of the selected models."""
        search_models = []

        if self.is_valid():
            model = self.cleaned_data['models']
            search_models.append(haystack_get_model(*model.split('.')))

        return search_models