# manager/views.py

from django.core.paginator import Paginator
from django.contrib import messages 
from .models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django import forms
from .forms import *


@login_required
def change_password(request):
    """
    View for changing user password.

    Returns:
        HttpResponse: The rendered change password page.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('user-account-update-password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change_password.html', {'form': form})


@login_required
def account_update(request):
    """
    View for updating user profile.

    Returns:
        HttpResponse: The rendered update profile page.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been successfully updated.')
            return redirect('user-account')  # Redirect to the profile page after successful update
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'user/update.html', {'form': form})


class RegistrationForm(UserCreationForm):
    """
    Form for user registration.

    Inherits:
        UserCreationForm: A form class for creating a new user.

    Attributes:
        email (EmailField): The email field for user registration.
        first_name (CharField): The first name field for user registration.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


def registration_view(request):
    """
    View for user registration.

    Returns:
        HttpResponse: The rendered registration page.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def account_view(request):
    """
    View for user account.

    Returns:
        HttpResponse: The rendered account page.
    """
    return render(request, "user/account.html")


def index(request):
    """
    View for the index page.

    Returns:
        HttpResponse: The rendered index page.
    """
    return render(request, "index.html")


def restricted(request):
    """
    View for the restricted page.

    Returns:
        HttpResponse: The rendered restricted page.
    """
    return render(request, "restricted.html")


@login_required
def delete_profile(request):
    """
    View for deleting user profile.

    Returns:
        HttpResponse: The rendered delete profile page.
    """
    if request.method == 'POST':
        # Delete the user's account
        request.user.delete()
        # Log out the user
        logout(request)
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('index')  # Redirect to the home page after deletion
    return render(request, 'user/delete_profile.html')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def user_list(request):
    """
    View for listing all users.

    Returns:
        HttpResponse: The rendered user list page.
    """
    # Get the search query from the request GET parameters
    search_query = request.GET.get('name')

    # If there's a search query, filter the queryset based on the name, username, and email
    if search_query:
        users = User.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        ).distinct()
    else:
        # If no search query, get all users
        users = User.objects.all()

    paginator = Paginator(users, 15)  # Show 15 users per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'user/user_list.html', {'page_obj': page_obj})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def user_detail(request, user_id):
    """
    View for displaying user details.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: The rendered user detail page.
    """
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user/user_detail.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def user_details(request, user_id):
    """
    View for displaying user details.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: The rendered user details page.
    """
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'user/user_details.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def remove_staff(request, user_id):
    """
    View for removing staff status from a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: Redirects to the user details page.
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_staff:
        user.is_staff = False
        user.save()
        messages.success(request, f"{user.username} is no longer a staff member.")
    return redirect('user_details', user_id=user_id)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def make_staff(request, user_id):
    """
    View for making a user a staff member.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: Redirects to the user details page.
    """
    user = get_object_or_404(User, pk=user_id)
    if not user.is_staff:
        user.is_staff = True
        user.save()
        messages.success(request, f"{user.username} is now a staff member.")
    return redirect('user_details', user_id=user_id)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def remove_superuser(request, user_id):
    """
    View for removing superuser status from a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: Redirects to the user details page.
    """
    user = get_object_or_404(User, pk=user_id)
    if user.is_superuser:
        user.is_superuser = False
        user.save()
        messages.success(request, f"{user.username} is no longer a superuser.")
    return redirect('user_details', user_id=user_id)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def make_superuser(request, user_id):
    """
    View for making a user a superuser.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: Redirects to the user details page.
    """
    user = get_object_or_404(User, pk=user_id)
    if not user.is_superuser:
        user.is_superuser = True
        user.save()
        messages.success(request, f"{user.username} is now a superuser.")
    return redirect('user_details', user_id=user_id)


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def delete_user(request, user_id):
    """
    View for deleting a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        HttpResponse: Redirects to the user details page.
    """
    user = get_object_or_404(User, pk=user_id)
    if user != request.user:  # Prevent deleting own account
        user.delete()
        messages.success(request, f"{user.username} has been deleted.")
        return redirect('all_users')
    else:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_details', user_id=user_id)
