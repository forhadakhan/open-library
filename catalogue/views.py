from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render
from .forms import *

# Create your views here.
def catalogue(request):
    return render(request, "catalogue/index.html")


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('catalogue')  # Redirect to catalogue view after adding book
        else:
            messages.error(request, 'Failed to add book.')
    else:
        form = BookForm()
    return render(request, 'catalogue/book_add.html', {'form': form})
