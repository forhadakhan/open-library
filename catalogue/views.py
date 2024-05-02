from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def catalogue(request):
    return render(request, "catalogue/index.html")


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/home/user/restricted/')
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


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    is_favorite = False
    if request.user.is_authenticated:
        # Check if the book is in the user's favorites
        is_favorite = FavoriteBook.objects.filter(user=request.user, book=book).exists()
    return render(request, 'catalogue/book_detail.html', {'book': book, 'is_favorite': is_favorite})


@login_required
def add_favorite_book(request, book_id):
    try:
        existing_favorite = FavoriteBook.objects.get(user=request.user, book_id=book_id)
        messages.info(request, 'Book is already in your favorites!')
    except FavoriteBook.DoesNotExist:
        favorite_book = FavoriteBook(user=request.user, book_id=book_id)
        favorite_book.save()
        messages.success(request, 'Book added to favorites!')
    return redirect('book_detail', book_id=book_id)


@login_required
def remove_favorite_book(request, book_id):
    try:
        favorite_book = FavoriteBook.objects.get(user=request.user, book_id=book_id)
        favorite_book.delete()
        messages.success(request, 'Book removed from favorites!')
    except FavoriteBook.DoesNotExist:
        messages.error(request, 'Book is not in your favorites!')
    return redirect('book_detail', book_id=book_id)


