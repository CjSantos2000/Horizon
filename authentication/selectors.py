from django.contrib.auth.models import User


def get_user_by_username(username: str) -> User:
    """Get a user instance by username."""
    if not username:
        raise ValueError("Username is required.")
    user = User.objects.filter(username=username).first()
    if not user:
        raise ValueError("User does not exist.")

    return user
