from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.db.models import Avg
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
    rating_range = range(1, 6)  # range from 1 to 5
    is_favorite = False
    reviews = Review.objects.filter(book=book)
    # Calculate overall rating
    overall_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if request.user.is_authenticated:
        # Check if the book is in the user's favorites
        is_favorite = FavoriteBook.objects.filter(user=request.user, book=book).exists()
    return render(request, 'catalogue/book_detail.html', {
        'book': book, 
        'is_favorite': is_favorite, 
        'reviews': reviews, 
        'rating_range': rating_range,
        'overall_rating': overall_rating,
    })


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


@login_required
def add_review(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Validate the rating
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5")
        except ValueError as e:
            return HttpResponseBadRequest("Invalid rating")

        review = Review(user=request.user, book=book, rating=rating, comment=comment)
        review.save()

        messages.success(request, 'Your review has been submitted successfully!')
        return redirect('book_detail', book_id=book_id)
    else:
        return redirect('book_detail', book_id=book_id)  # Redirect if not a POST request


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    # Check if the request user is the owner of the review or is a superuser
    if request.user == review.user or request.user.is_superuser:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this review.')
    
    return redirect('book_detail', book_id=review.book.id)

