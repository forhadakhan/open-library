from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path('book/all/', views.all_books, name='all_books'),
    path('book/add/', views.add_book, name='add_book'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/<int:book_id>/add-as-favorite/', views.add_favorite_book, name='add_favorite_book'),
    path('book/<int:book_id>/remove-from-favorite/', views.remove_favorite_book, name='remove_favorite_book'),
]

