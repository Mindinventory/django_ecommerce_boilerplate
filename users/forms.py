from django import forms
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ecommerce.email.email import send_mail_from_system
from users.models import ForgotPassword


class UserRegisterForm(UserCreationForm):
    """
        A form that creates a user, with no privileges.
    """
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'E-mail'}))
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Username'}))
    password1 = forms.CharField(strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'new-password', "class": 'form-control',
                                           'placeholder': 'Password'}),
                                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', "class": 'form-control', 'placeholder': 'Confirm password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    mobile_no = forms.CharField(min_length=12, max_length=15, required=False,
                                widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Mobile no.'}))
    alt_mobile_no = forms.CharField(min_length=12, max_length=15, required=False,
                                    widget=forms.TextInput(
                                        attrs={"class": 'form-control', 'placeholder': 'Alternate mobile no.'}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2", "mobile_no",
                  "alt_mobile_no"]


class LoginForm(AuthenticationForm):
    """
        A form that allows user to login with correct username and password.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password', "class": 'form-control',
                                          'placeholder': 'Password'}))







class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'First name',
                                                               }))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Last name',
                                                              }))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(
                                 attrs={"class": 'form-control', 'placeholder': 'E-mail'}))
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(
                                   attrs={"class": 'form-control', 'placeholder': 'Username'}))
    mobile_no = forms.CharField(min_length=12, max_length=15, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Mobile no'}))
    alt_mobile_no = forms.CharField(min_length=12, max_length=15, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Alternate Mobile No.'}))
    address_one = forms.CharField(max_length=250, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Address 1', 'label': 'Address 1'}))
    address_two = forms.CharField(max_length=250, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Address 2', 'label': 'Address 2'}))
    zipcode = forms.CharField(max_length=25, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'zipcode'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, "placeholder": "Old password",
                   'class': 'form-control'}
        ),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "New password", 'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "placeholder": "Confirm password", 'class': 'form-control'}),
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise ValidationError("Please enter valid email")


class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )
