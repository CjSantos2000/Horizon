from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from HorizonApp import errors


# User Module


def create_user_as_admin(
    *,
    user: User,
    email: str,
    password: str,
    username: str,
    first_name: str,
    last_name: str,
) -> User:
    """
    This function receives a request data and creates a user as admin.
    @params user (User): The user.
    @params email (str): The email.
    @params password (str): The password.
    @params confirm_password (str): The confirm password.
    @out (User): The created user.
    """

    if not user.is_superuser:
        error_code, error_msg = errors.USER_NO_ACCESS
        raise errors.InvestorAppException(error_msg, code=error_code)

    if not email:
        error_code, error_msg = errors.EMAIL_REQUIRED
        raise errors.InvestorAppException(error_msg, code=error_code)

    if not password:
        error_code, error_msg = errors.PASSWORD_REQUIRED
        raise errors.InvestorAppException(error_msg, code=error_code)

    if User.objects.filter(email=email).exists():
        error_code, error_msg = errors.EMAIL_DUPLICATE
        raise errors.InvestorAppException(error_msg, code=error_code)

    # [TODO] -> No more set password user will set their own password
    try:
        validate_password(password)

    except:
        error_code, error_msg = errors.INVALID_PASSWORD
        raise errors.InvestorAppException(error_msg, code=error_code)

    user = User.objects.create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    user.set_password(password)
    # [TODO] -> Email Sending Confirmation
    # user.is_active = False
    user.save()

    return user
