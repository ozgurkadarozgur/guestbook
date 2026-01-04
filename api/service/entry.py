from django.db import transaction

from api import models
from api.dto.entry import PaginatedEntriesDTO, EntryDTO
from api.dto.user import UserDTO, UserEntryStatusDTO
from api.service.entry_cache import increment_user_entry_count_on_cache, cache_entry_as_user_last_entry, \
    get_user_last_entry_from_cache, get_user_entry_count_from_cache
from api.service.user import get_or_create_user_by_name, get_all_users

DEFAULT_ENTRIES_PAGINATION_LIMIT = 3


def create_entry(subject: str, message: str, user_name: str):
    with transaction.atomic():
        user_dto = get_or_create_user_by_name(user_name)

        created_entry = models.Entry.objects.create(
            subject=subject,
            message=message,
            user_id=user_dto.id,
        )

    if user_dto is not None and created_entry is not None:
        increment_user_entry_count_on_cache(user_dto.id)
        cache_entry_as_user_last_entry(user_dto.id, created_entry.subject, created_entry.message)


def get_entries(next_cursor: int | None = None, previous_cursor: int | None = None, limit: int | None = None) -> PaginatedEntriesDTO:
    if next_cursor is not None and previous_cursor is not None:
        raise RuntimeError("next_cursor and previous_cursor can not be provided at the same time.")

    if limit is None:
        limit = DEFAULT_ENTRIES_PAGINATION_LIMIT

    entries_qs = models.Entry.objects.select_related("user")

    if next_cursor is not None:
        entries_qs = entries_qs.filter(id__lt=next_cursor)

    if previous_cursor is not None:
        entries_qs = entries_qs.filter(id__gte=previous_cursor)

    entries_result = list(entries_qs.order_by("-id")[:limit].values("id", "subject", "message", "created_at", "user__id", "user__name"))

    entries = []
    for item in entries_result:
        entries.append(
            EntryDTO(
                id=item["id"],
                subject=item["subject"],
                message=item["message"],
                created_at=item["created_at"],
                user=UserDTO(
                    id=item["user__id"],
                    name=item["user__name"],
                )
            )
        )

    new_next_cursor = None
    if len(entries) == limit:
        new_next_cursor = entries[-1].id

    return PaginatedEntriesDTO(
        entries=entries,
        next_cursor=new_next_cursor,
        previous_cursor=next_cursor,
    )


def get_users_entry_statuses() -> list[UserEntryStatusDTO]:
    all_users = get_all_users()

    users_entry_statuses: list[UserEntryStatusDTO] = []
    for user in all_users:
        user_last_entry = get_user_last_entry_from_cache(user.id)
        user_entry_count = get_user_entry_count_from_cache(user.id)

        last_entry_text = None
        if user_last_entry is not None:
            subject = user_last_entry["subject"]
            message = user_last_entry["message"]
            last_entry_text = f"{subject} | {message}"

        users_entry_statuses.append(
            UserEntryStatusDTO(
                name=user.name,
                last_entry=last_entry_text,
                total_entry_count=user_entry_count,
            )
        )

    return users_entry_statuses
