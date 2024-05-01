from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.registration_view, name="register"),
    path("user/restricted/", views.restricted, name="restricted"),
    path("user/account/", views.account_view, name="user-account"),
    path("user/account/update/", views.account_update, name="user-account-update"),
    path("user/account/update/password/", views.change_password, name="user-account-update-password"),
]

