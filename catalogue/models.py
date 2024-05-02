from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField('image', blank=True)
    publication_date = models.DateField(blank=True, null=True) 
    upload_date = models.DateTimeField(auto_now_add=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title


class FavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved book '{self.book.title}' by {self.user.username}"
