from django.forms import ModelForm
from django import forms
from .models import *

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover_image', 'publication_date', 'isbn']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }

