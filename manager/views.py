# manager/views.py

from django.core.paginator import Paginator
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django import forms
from .forms import *



@login_required
def change_password(request):
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
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


def registration_view(request):
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
    return render(request, "user/account.html")


def index(request):
    return render(request, "index.html")


def restricted(request):
    return render(request, "restricted.html")


@login_required
def delete_profile(request):
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
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user/user_detail.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/home/user/restricted/')
def user_details(request, user_id):
    pass 
