# forms.py
from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            # This makes the input transparent so we can style the container
            'class': 'w-full bg-transparent border-none focus:ring-0 text-gray-700 h-14 px-4 text-lg outline-none',
            'placeholder': 'جستجو بر اساس نام، کدملی یا شماره پرونده...'
        })
    )
