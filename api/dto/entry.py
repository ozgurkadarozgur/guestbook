from dataclasses import dataclass
from datetime import datetime

from api.dto.user import UserDTO


@dataclass(frozen=True)
class EntryDTO:
    id: int
    subject: str
    message: str
    created_at: datetime
    user: UserDTO


@dataclass(frozen=True)
class PaginatedEntriesDTO:
    entries: list[EntryDTO]
    next_cursor: str | None
    previous_cursor: str | None
