from django import forms
from django.contrib.auth import password_validation,authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, \
    SetPasswordForm, AuthenticationForm
from users.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


class UserRegisterForm(UserCreationForm):
    """
        A form that creates a user, with no privileges.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'current-password', "class": 'form-control',
                                           'placeholder': 'Password'}))
    password2 = forms.CharField(strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'new-password', "class": 'form-control',
                                           'placeholder': 'Confirm Password'}))
    mobile_no = forms.CharField(min_length=12, max_length=15, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Mobile no'}))
    alt_mobile_no = forms.CharField(min_length=12, max_length=15, required=False, widget=forms.TextInput(
        attrs={"class": 'form-control', 'placeholder': 'Alternate Mobile no'}))

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "mobile_no", "alt_mobile_no"]


class LoginForm(AuthenticationForm):
    """
        A form that allows user to login with correct username and password.
    """
    error_messages = {
        "invalid_login":
            "Please enter a correct username and password."
        ,
        "inactive": "This account is inactive.",
    }

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password', "class": 'form-control',
                                          'placeholder': 'Password'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                messages.error(self.request, "Invalid login credentials")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class EditProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'First name',
                                                               }))
    last_name = forms.CharField(max_length=30,
                                widget=forms.TextInput(attrs={"class": 'form-control', 'placeholder': 'Last name',
                                                              }))
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(
                                   attrs={"class": 'form-control', 'placeholder': 'Email'}))
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
