from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path('book/add/', views.add_book, name='add_book'),
]

