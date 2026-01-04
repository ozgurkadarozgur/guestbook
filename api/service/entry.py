from django.db import transaction

from api import models
from api.dto.entry import PaginatedEntriesDTO, EntryDTO
from api.dto.user import UserDTO
from api.service.user import get_or_create_user_by_name

DEFAULT_ENTRIES_PAGINATION_LIMIT = 3

def create_entry(subject: str, message: str, user_name: str):
    with transaction.atomic():
        user_dto = get_or_create_user_by_name(user_name)

        models.Entry.objects.create(
            subject=subject,
            message=message,
            user_id=user_dto.id,
        )

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


