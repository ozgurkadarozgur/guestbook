from typing import NamedTuple, TypedDict

from api.transport.response.pagination import PaginationLinksResponse, SerializedPaginationLinksResponse
from api.transport.response.user import SerializedUserResponse, UserResponse


class SerializedEntryResponse(TypedDict):
    user: SerializedUserResponse
    subject: str
    message: str


class EntryResponse(NamedTuple):
    user: UserResponse
    subject: str
    message: str

    def serialize(self) -> SerializedEntryResponse:
        return SerializedEntryResponse(
            user=self.user.serialize(),
            subject=self.subject,
            message=self.message,
        )


class SerializedPaginatedEntriesResponse(TypedDict):
    links: SerializedPaginationLinksResponse
    entries: list[SerializedEntryResponse]


class PaginatedEntriesResponse(NamedTuple):
    links: PaginationLinksResponse
    entries: list[EntryResponse]

    def serialize(self) -> SerializedPaginatedEntriesResponse:
        serialized_entries = []
        for entry in self.entries:
            serialized_entries.append(entry.serialize())

        return SerializedPaginatedEntriesResponse(
            links=self.links.serialize(),
            entries=serialized_entries,
        )
