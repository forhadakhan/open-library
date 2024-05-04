# manager/authentication.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate using either their username or email.
    
    This backend checks if the input username is an email address. If it is, it attempts to find a user with
    that email address in the database. If not found, it falls back to checking if the input username is a
    username and attempts to find a user with that username. If the user is found and the provided password
    is correct, the user is authenticated.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user with either their username or email address and password.
        
        Args:
            request: The request object.
            username: The username or email address of the user.
            password: The password of the user.
            **kwargs: Additional keyword arguments.
        
        Returns:
            The authenticated user object if authentication is successful, None otherwise.
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                UserModel().set_password(password)
        if user.check_password(password):
            return user
