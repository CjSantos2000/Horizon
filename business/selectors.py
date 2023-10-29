from typing import List
from django.contrib.auth.models import User


def get_users_by_ids_as_admin(
    *,
    ids: List[int],
) -> List[User]:
    """
    This function receives a request data and returns users by ids as admin.
    @params ids (List[int]): The ids.
    @out (List[User]): The users.
    """
    return User.objects.filter(id__in=ids)
