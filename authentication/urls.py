from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("add-user/", views.RegistrationView.as_view(), name="add-user"),
    path(
        "validate-username/",
        csrf_exempt(views.UsernameValidationView.as_view()),
        name="validate-username",
    ),
    path(
        "validate-email/",
        csrf_exempt(views.EmailValidationView.as_view()),
        name="validate-email",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("users/", views.UserView.as_view(), name="users"),
]
