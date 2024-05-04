from django import forms
from .models import User

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Inherits:
        forms.ModelForm: A form class for creating and updating Django model instances.

    Attributes:
        Meta:
            model (User): The user model associated with this form.
            fields (list): The list of fields to include in the form.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ChangePasswordForm(forms.Form):
    """
    Form for changing user password.

    Inherits:
        forms.Form: A generic form class.

    Attributes:
        old_password (CharField): The field for entering the old password.
        new_password1 (CharField): The field for entering the new password.
        new_password2 (CharField): The field for confirming the new password.
    """
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)
