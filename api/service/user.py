from api import models
from api.dto.user import UserDTO

DEFAULT_USERS_PAGINATION_LIMIT = 1000

def get_or_create_user_by_name(name: str) -> UserDTO:
    user, _ = models.User.objects.get_or_create(name=name)

    return UserDTO(
        id=user.id,
        name=user.name,
    )


def get_all_users() -> list[UserDTO]:
    users: list[UserDTO] = []

    cursor = None
    while True:
        users_qs = models.User.objects.order_by("id")

        if cursor is not None:
            users_qs = users_qs.filter(id__gt=cursor)

        db_users = list(users_qs[:DEFAULT_USERS_PAGINATION_LIMIT])
        if len(db_users) == 0:
            break

        cursor = db_users[-1].id

        for db_user in db_users:
            users.append(
                UserDTO(
                    id=db_user.id,
                    name=db_user.name,
                )
            )

    return users
