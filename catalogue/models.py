from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    """
    Represents a book in the system.

    Attributes:
        title (str): The title of the book.
        author (str): The author(s) of the book.
        genre (str): The genre of the book.
        description (str, optional): A description of the book. Defaults to empty string.
        cover_image (CloudinaryField, optional): The cover image of the book. Defaults to None.
        publication_date (DateField, optional): The publication date of the book. Defaults to None.
        upload_date (DateTimeField): The date and time when the book record was created.
        isbn (str, optional): The International Standard Book Number (ISBN) of the book. Defaults to None.

    Methods:
        __str__: Returns a string representation of the book instance.
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField('image', blank=True)
    publication_date = models.DateField(blank=True, null=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the book instance.

        Returns:
            str: The title of the book.
        """
        return self.title


class FavoriteBook(models.Model):
    """
    Represents a favorite book saved by a user.

    Attributes:
        user (ForeignKey): The user who saved the book.
        book (ForeignKey): The book that was saved.
        saved_date (DateTimeField): The date and time when the book was saved.

    Methods:
        __str__: Returns a string representation of the favorite book instance.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the favorite book instance.

        Returns:
            str: A formatted string indicating the saved book's title and the user who saved it.
        """
        return f"Saved book '{self.book.title}' by {self.user.username}"


class Review(models.Model):
    """
    Represents a review of a book by a user.

    Attributes:
        user (ForeignKey): The user who wrote the review.
        book (ForeignKey): The book being reviewed.
        rating (int): The rating given to the book, ranging from 0 to 5.
        comment (str): The comment or review text.
        created_at (DateTimeField): The date and time when the review was created.
        updated_at (DateTimeField): The date and time when the review was last updated.

    Methods:
        __str__: Returns a string representation of the review instance.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the review instance.

        Returns:
            str: A formatted string indicating the book title and the user who wrote the review.
        """
        return f"Review for '{self.book.title}' by {self.user.username}"




#########################
# Abandoned Features
#########################

# class ReadingProgress(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     # Track progress (e.g., pages read, percentage, completion status)
#     pages_read = models.IntegerField(default=0)
#     is_completed = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('user', 'book')  # Ensure one progress record per user/book

#     def __str__(self):
#         return f"{self.user.username} - {self.book.title} ({self.pages_read} pages read)"


# class BorrowRequest(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey('Book', on_delete=models.CASCADE)
#     request_date = models.DateTimeField(auto_now_add=True)
#     expected_return_date = models.DateTimeField()

#     PENDING = 'P'
#     APPROVED = 'A'
#     REJECTED = 'R'
#     STATUS_CHOICES = [
#         (PENDING, 'Pending'),
#         (APPROVED, 'Approved'),
#         (REJECTED, 'Rejected'),
#     ]
#     status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

#     def __str__(self):
#         return f"Borrow request for '{self.book.title}' by {self.user.username}"


# class BorrowRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     borrow_request = models.OneToOneField(BorrowRequest, on_delete=models.CASCADE)
#     borrow_date = models.DateTimeField(auto_now_add=True)
#     expected_return_date = models.DateTimeField()
#     return_date = models.DateTimeField(null=True, blank=True)
#     returned = models.BooleanField(default=False)
#     return_status = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(self):
#         return f"Borrow record for '{self.borrow_request.book.title}' by {self.user.username}"

#     @property
#     def is_overdue(self):
#         if self.return_date is None:
#             return False
#         return self.return_date > self.expected_return_date
