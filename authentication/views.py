import json
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from validate_email import validate_email
from .services import create_user_as_admin


# Create your views here.


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data.get("email")

        if not validate_email(email):
            return JsonResponse({"email_error": "Email is invalid"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "Sorry, email is already taken"},
                status=409,
            )
        return JsonResponse({"email_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "Username should only contain alphanumeric characters"
                },
                status=400,
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "Username is already taken "}, status=400
            )
        return JsonResponse({"username_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, "users/add-user.html")

    def post(self, request):
        # Get user data
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        context = {"fieldValues": request.POST}

        # Validate user data
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, "Password too short")
                    return render(request, "users/add-user.html", context)

                try:
                    user = create_user_as_admin(
                        user=request.user,
                        email=email,
                        password=password,
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    # [TODO] -> Setup Email Confirmation

                    # email_subject = "Activate your account"
                    # email_body = ""
                    # email = EmailMessage(
                    #     email_subject,
                    #     email_body,
                    #     "noreply@semicolon.com",
                    #     [user.email],
                    # )
                    # email.send(fail_silently=False)
                    messages.success(request, "Account created successfully")
                    return redirect("users")
                except Exception as e:
                    messages.error(request, e)
                    return render(request, "users/add-user.html", context)

            messages.error(request, "Email already exists")

        messages.error(request, "Username already exists")

        return render(request, "users/add-user.html", context)


# [TODO] -> Setup Email Confirmation
class VerificationView(View):
    def get(self, request, uidb64, token):
        return render(request, "authentication/verification.html")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username}")
                    return redirect("dashboard")

                messages.error(
                    request, "Account is not active, please check your email"
                )
                return render(request, "authentication/login.html")

            messages.error(request, "Invalid Crenedtials, Try Again")
            return render(request, "authentication/login.html")

        messages.error(request, "Please fill all fields")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out")
        return render(request, "authentication/login.html")


class UserView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, "users/index.html", {"users": users})
