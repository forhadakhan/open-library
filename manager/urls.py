from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.registration_view, name="register"),
    path("user/account/", views.account_view, name="user-account"),
]

