# catalogue/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.db.models import Avg, Q, F
from .models import Book, FavoriteBook, Review
from .forms import BookForm
from .utils import dashboard_menu_options, validate_rating


# Views

def catalogue(request):
    """
    Renders the catalogue index page.

    Returns:
        HttpResponse: The rendered catalogue index page.
    """
    menu_options = dashboard_menu_options
    return render(request, "catalogue/index.html", {'menu_options': menu_options})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/home/user/restricted/')
def add_book(request):
    """
    Handles the addition of a new book.
    
    Args:
        request: HTTP request object.

    Returns:
        HttpResponse: The rendered book addition page.
    """
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


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url='/home/user/restricted/')
def delete_book(request, book_id):
    """
    Handles the deletion of a book.

    Args:
        request: HTTP request object.
        book_id (int): The ID of the book to delete.

    Returns:
        HttpResponse: Rendered template with confirmation of book deletion.
        HttpResponseRedirect: Redirects to the book list page after successful deletion.
        Http404: If the requested book does not exist.
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('all_books')


def all_books(request):
    """
    Renders the page displaying all books.

    Returns:
        HttpResponse: The rendered page displaying all books.
    """
    # Get sorting parameters from the request
    sort_by = request.GET.get('sort_by', 'default')  # Default sorting option
    order_by = request.GET.get('order_by', 'asc')  # Default order: ascending

    # Define the sorting options
    sorting_options = {
        'default': 'id',  # Default sorting by book ID
        'publication_date': 'publication_date',
        'upload_date': 'upload_date',
        'rating': 'overall_rating',  # Assuming you have overall_rating field for books
    }

    # Get the field to sort by based on the selected option
    sort_field = sorting_options.get(sort_by, 'id')

    # Determine the ordering based on the selected order
    if order_by == 'desc':
        sort_field = F(sort_field).desc()

    # Get all books queryset with rating
    all_books_list = Book.objects.annotate(overall_rating=Avg('review__rating'))

    # Sort the queryset based on the selected sorting option
    if sort_by != 'rating':  # For 'rating', sorting is handled separately due to aggregation
        all_books_list = all_books_list.order_by(sort_field)

    # For rating, sort by annotation since it requires aggregation
    if sort_by == 'rating':
        all_books_list = all_books_list.annotate(overall_rating=Avg('review__rating'))
        if order_by == 'desc':
            all_books_list = all_books_list.order_by('-overall_rating')
        else:
            all_books_list = all_books_list.order_by('overall_rating')

    # Paginate the sorted queryset
    paginator = Paginator(all_books_list, 15)  # Show 15 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalogue/books.html', {
        'page_obj': page_obj,
        'sort_by': sort_by,
        'order_by': order_by,
    })


def search_books(request):
    """
    Renders the page displaying search results for books.

    Returns:
        HttpResponse: The rendered page displaying search results for books.
    """
    query = request.GET.get('q')
    if query is None:
        return redirect('all_books')

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        ).distinct()
    else:
        books = []

    paginator = Paginator(books, 15)  # Show 15 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalogue/search.html', {'page_obj': page_obj, 'query': query})


def book_detail(request, book_id):
    """
    Renders the page displaying details of a specific book.

    Returns:
        HttpResponse: The rendered page displaying details of a specific book.
    """
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
    """
    Adds a book to the user's favorites.

    Returns:
        HttpResponse: Redirects to the book detail page.
    """
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
    """
    Removes a book from the user's favorites.

    Returns:
        HttpResponse: Redirects to the book detail page.
    """
    try:
        favorite_book = FavoriteBook.objects.get(user=request.user, book_id=book_id)
        favorite_book.delete()
        messages.success(request, 'Book removed from favorites!')
    except FavoriteBook.DoesNotExist:
        messages.error(request, 'Book is not in your favorites!')
    return redirect('book_detail', book_id=book_id)


@login_required
def add_review(request, book_id):
    """
    Adds a review for a book.

    Returns:
        HttpResponse: Redirects to the book detail page.
    """
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=book_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Validate the rating
        try:
            rating = validate_rating(rating)
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
    """
    Deletes a review.

    Returns:
        HttpResponse: Redirects to the book detail page.
    """
    review = get_object_or_404(Review, pk=review_id)

    # Check if the request user is the owner of the review or is a superuser
    if request.user == review.user or request.user.is_superuser:
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this review.')

    return redirect('book_detail', book_id=review.book.id)


@login_required
def favorite_books(request):
    """
    Renders the page displaying the user's favorite books.

    Returns:
        HttpResponse: The rendered page displaying the user's favorite books.
    """
    favorite_books_list = FavoriteBook.objects.filter(user=request.user)
    paginator = Paginator(favorite_books_list, 15)  # Show  15 favorite books per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalogue/favorite_books.html', {'page_obj': page_obj})

