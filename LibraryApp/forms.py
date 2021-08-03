from django import forms


class SearchForm(forms.Form):
    search_field = forms.CharField(
        max_length=200,
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'search-box',
            'placeholder': 'Search...'
        }))
