from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path('book/all/', views.all_books, name='all_books'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/add/', views.add_book, name='add_book'),
]

