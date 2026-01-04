from typing import NamedTuple, TypedDict


class SerializedPaginationLinksResponse(TypedDict):
    next_link: str | None
    previous_link: str | None


class PaginationLinksResponse(NamedTuple):
    next_link: str | None
    previous_link: str | None

    def serialize(self) -> SerializedPaginationLinksResponse:
        return SerializedPaginationLinksResponse(
            next_link=self.next_link,
            previous_link=self.previous_link,
        )
