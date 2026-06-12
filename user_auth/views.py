from django.shortcuts import render, redirect
from contact_app.models import PasswordResetToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


# Create your views here.
# ------------------------------------------createuser---------------------------------------------------------
def createuser(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not phone.isdigit():
            return render(request, "auth/createuser.html", {
                "error": "Phone number must contain only digits",
                "name": name,
                "email": email,
                "phone": phone,
                "username": username,
            })

        if len(phone) != 10:
            return render(request, "auth/createuser.html", {
                "error": "Phone number must be exactly 10 digits",
                "name": name,
                "email": email,
                "phone": phone,
                "username": username,
            })

        if password != confirm_password:
            return render(request, "auth/createuser.html", {
                "error": "Passwords do not match",
                "name": name,
                "email": email,
                "phone": phone,
                "username": username,
            })

        if User.objects.filter(username=username).exists():
            return render(request, "auth/createuser.html", {
                "error": "Username already exists",
                "name": name,
                "email": email,
                "phone": phone,
                "username": username,
            })
        
        if User.objects.filter(email=email).exists():
            return render(request, "auth/createuser.html", {
                "error": "Email already exists",
                "name": name,
                "phone": phone,
                "username": username,
            })
        
        if User.objects.filter(phone_number=phone).exists():
            return render(request, "auth/createuser.html", {
                "error": "Phone number already exists",
                "name": name,
                "email": email,
                "username": username,
            })

        User.objects.create_user(
            username=username,
            email=email,
            phone_number=phone,
            password=password
        )

        return render(
            request,
            "auth/createuser.html",
            {"success": "User created successfully"}
        )

    return render(request, "auth/createuser.html")

# ------------------------------------------login---------------------------------------------------------
def login_page(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            return render(
                request,
                "auth/login.html",
                {"error": "Username does not exist"}
            )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return render(
                request,
                "auth/login.html",
                {"error": "Incorrect password"}
            )

        login(request, user)
        return redirect("index")

    return render(request, "auth/login.html")

# ------------------------------------------Change password ---------------------------------------------------------
@login_required
def change_password(request):
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(request, "auth/change_password.html", {"error": "Passwords do not match"})

        request.user.set_password(new_password)
        request.user.save()
        return redirect("login")

    return render(request, "auth/change_password.html")

# ─── Forgot Password: send reset link via Mailtrap ───────────────────────────
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "auth/forgot_password.html", {
                "error": "No account found with that email address."
            })

        # Create a fresh token (delete old ones for this user first)
        PasswordResetToken.objects.filter(user=user).delete()
        reset_token = PasswordResetToken.objects.create(user=user)

        # Build the reset link
        reset_link = request.build_absolute_uri(
            f"/reset-password/{reset_token.token}/"
        )

        # Send email via Mailtrap
        send_mail(
            subject="Password Reset Request – Contact App",
            message=(
                f"Hi {user.username},\n\n"
                f"You requested a password reset. Click the link below to set a new password:\n\n"
                f"{reset_link}\n\n"
                f"This link expires in 1 hour. If you did not request this, ignore this email.\n\n"
                f"– Contact App Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return render(request, "auth/forgot_password.html", {
            "success": "A password reset link has been sent to your email."
        })

    return render(request, "auth/forgot_password.html")


# ─── Reset Password: validate token, set new password ─────────────────────────

def reset_password(request, token):
    try:
        reset_obj = PasswordResetToken.objects.get(token=token, is_used=False)
    except PasswordResetToken.DoesNotExist:
        return render(request, "auth/reset_password.html", {
            "error": "This reset link is invalid or has already been used."
        })

    # Check expiry (1 hour)
    expiry_time = reset_obj.created_at + timedelta(hours=1)
    if timezone.now() > expiry_time:
        reset_obj.delete()
        return render(request, "auth/reset_password.html", {
            "error": "This reset link has expired. Please request a new one."
        })

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(request, "auth/reset_password.html", {
                "error": "Passwords do not match.",
                "token": token,
            })

        user = reset_obj.user
        user.set_password(new_password)
        user.save()

        reset_obj.is_used = True
        reset_obj.save()

        return render(request, "auth/reset_password.html", {
            "success": "Password changed successfully! You can now log in."
        })

    return render(request, "auth/reset_password.html", {"token": token})

def logout_page(request):
    logout(request)
    return redirect("login")
