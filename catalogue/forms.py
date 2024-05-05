# catalogue/forms.py

from cloudinary.forms import CloudinaryFileField
from django.forms import ModelForm
from django import forms
from .models import Book

class BookForm(ModelForm):
    """
    Form for creating and updating book records.

    Inherits:
        ModelForm: A form class that automatically generates fields from a Django model.

    Attributes:
        Meta:
            model (Book): The model class associated with this form.
            fields (list): The list of fields to include in the form.
            widgets (dict): Custom widgets for specific form fields.

    """
    cover_image = CloudinaryFileField()
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'cover_image', 'publication_date', 'isbn']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }

