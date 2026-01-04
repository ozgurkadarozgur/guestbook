from api import models
from api.dto.user import UserDTO


def get_or_create_user_by_name(name: str) -> UserDTO:
    user, _ = models.User.objects.get_or_create(name=name)

    return UserDTO(
        id=user.id,
        name=user.name,
    )