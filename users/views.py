from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ecommerce.settings import EMAIL_HOST_USER
from store.tasks import send_reset_email_task
from users.forms import UserRegisterForm, EditProfileForm, LoginForm, ForgotPasswordForm, \
    ResetPasswordForm, ChangePasswordForm
from users.models import Profile, ShippingAddress, ForgotPassword, User
from ecommerce import logger
from store.utils import cookiecart


def register(request):
    """
        Registers new user in the system and redirects them to the login page.
    """
    try:
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            obj = form.save()
            obj.email = obj.username
            obj.save()
            if form.cleaned_data['mobile_no'] or form.cleaned_data['alt_mobile_no']:
                Profile.objects.create(user=obj, mobile_no=form.cleaned_data.get('mobile_no', None),
                                       alt_mobile_no=form.cleaned_data.get('alt_mobile_no', None))
            logger.info("User registered successfully")
            return redirect("login")
        return render(request, "registration.html", {"form": form, "cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in registering user -- {0}".format(ex.args))
        return render(request, template_name="registration.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})


def login(request):
    """
        Logs in the user in the system after successfully registered and redirects to home page.
    """
    try:
        form = LoginForm(request=request, data=request.POST or None)
        if form.is_valid():
            auth_login(request, form.get_user())
            # After login, redirects to specified page in the URL.
            if "next" in request.GET:
                return redirect(request.GET.get('next'))
            logger.info("User with name {0} logged in successfully".format(form.get_user()))
            return redirect("home")
        logger.info("User entered invalid login credentials")
        return render(request, "login.html", {"form": form, "cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in logging in  user -- {0}".format(ex.args))
        return render(request, template_name="login.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})


@login_required(login_url="login")
def edit_profile(request):
    """
        Allows user to view and edit profile.
    """
    try:
        form = EditProfileForm(request.POST or None,
                               initial={
                                   "first_name": request.user.first_name,
                                   "last_name": request.user.last_name,
                                   "username": request.user.username,
                                   "address_one": request.user.user_shipping_address.address_one if hasattr(
                                       request.user, "user_shipping_address") else None,
                                   "address_two": request.user.user_shipping_address.address_two if hasattr(
                                       request.user, "user_shipping_address") else None,
                                   "zipcode": request.user.user_shipping_address.zipcode
                                   if hasattr(request.user, "user_shipping_address") else None,
                                   "mobile_no": request.user.user_profile.mobile_no
                                   if hasattr(request.user, "user_profile") else None,
                                   "alt_mobile_no": request.user.user_profile.alt_mobile_no
                                   if hasattr(request.user, "user_profile") else None,
                               }
                               )
        if form.is_valid():
            request.user.first_name, request.user.last_name, request.user.username, request.user.email \
                = form.cleaned_data.get('first_name'), form.cleaned_data.get('last_name'), \
                  form.cleaned_data.get('username'), form.cleaned_data.get('username')
            request.user.save()
            Profile.objects.update_or_create(user=request.user,
                                             defaults={"mobile_no": form.cleaned_data.get('mobile_no'),
                                                       "alt_mobile_no": form.cleaned_data.get('alt_mobile_no')})
            ShippingAddress.objects.update_or_create(user=request.user, defaults={"address_one": form.cleaned_data.get(
                'address_one'), "address_two": form.cleaned_data.get('address_two'),
                "zipcode": form.cleaned_data.get('zipcode')})
            logger.info("Profile of user with name {0} edited successfully".format(request.user.username))
            return redirect('home')
        return render(request, 'edit_profile.html', {"form": form, "cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in editing profile-- {0}".format(ex.args))
        return render(request, template_name="edit_profile.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})


@login_required(login_url="login")
def change_password(request):
    """
        Allows user to change password and allow login with new password.
    """
    try:
        form = ChangePasswordForm(request.user, request.POST or None)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password1'])
            request.user.save()
            # Updates password in current session and logs out current user from all other sessions
            update_session_auth_hash(request, request.user)
            logger.info("Password of user with name {0} changed successfully".format(request.user.username))
            return redirect('home')
        return render(request, "change_password.html",
                      {"form": form, "cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in changing password - {0}".format(ex.args))
        return render(request, template_name="change_password.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})


def forgot_password(request):
    """
        Sends an email with one-use only reset password link to user.
    """
    try:
        form = ForgotPasswordForm(request.POST or None)
        if form.is_valid():
            user = get_object_or_404(User, email=form.cleaned_data["email"])
            ForgotPassword.objects.create(user=user)
            send_reset_email_task(subject="Reset your password", context={"user": user}, from_email=EMAIL_HOST_USER,
                                  to=[user.email], html_email_template_name="email_template.html")
            logger.info("Reset password link sent to user successfully")
            messages.success(request,
                             message="An email with reset password link is sent to you. Please check your inbox.",
                             )
            return redirect('login')
        return render(request, template_name="forgot_password.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in sending reset password link  -- {0}".format(ex.args))
        return render(request, template_name="forgot_password.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})


def reset_password(request, id):
    user = get_object_or_404(User, pk=id)
    try:
        if ForgotPassword.objects.filter(user=user).exists():
            form = ResetPasswordForm(user, request.POST or None)
            if form.is_valid():
                ForgotPassword.objects.get(user=user).delete()
                logger.info("Password reset successfully")
                return redirect("password_reset_complete")
            return render(request, template_name="reset_password.html",
                          context={"form": form, "cartitems": cookiecart(request)['cartitems']})
        return render(request, template_name="link_expired.html",
                      context={"cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in resetting password  -- {0}".format(ex.args))
        return render(request, template_name="reset_password.html",
                      context={"form": form, "cartitems": cookiecart(request)['cartitems']})


def password_reset_complete(request):
    try:
        return render(request, template_name="password_reset_complete.html",
                      context={"cartitems": cookiecart(request)['cartitems']})
    except Exception as ex:
        logger.info("Exception raised in redirecting to password reset complete  -- {0}".format(ex.args))
        return render(request, template_name="reset_password.html",
                      context={"cartitems": cookiecart(request)['cartitems']}
                      )


@login_required(login_url="login")
def logout(request):
    """
        Logs out the user if they are logged in.
    """
    auth_logout(request)
    logger.info("User logged out successfully")
    messages.success(request, message="User logged out successfully")
    return redirect("login")
