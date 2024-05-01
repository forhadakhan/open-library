from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
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


def all_books(request):
    all_books_list = Book.objects.all()
    paginator = Paginator(all_books_list, 30)  # Show 30 books per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalogue/books.html', {'page_obj': page_obj})

