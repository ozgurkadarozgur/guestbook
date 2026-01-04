from typing import TypedDict, NamedTuple


class SerializedUserResponse(TypedDict):
    name: str


class UserResponse(NamedTuple):
    name: str

    def serialize(self) -> SerializedUserResponse:
        return SerializedUserResponse(
            name=self.name,
        )


class SerializedUserEntryStatusResponse(TypedDict):
    username: str
    last_entry: str
    total_entry_count: int


class UserEntryStatusResponse(NamedTuple):
    username: str
    last_entry: str
    total_entry_count: int

    def serialize(self) -> SerializedUserEntryStatusResponse:
        return SerializedUserEntryStatusResponse(
            username=self.username,
            last_entry=self.last_entry,
            total_entry_count=self.total_entry_count,
        )


class SerializedAllUsersEntryStatusesResponse(TypedDict):
    users: list[SerializedUserEntryStatusResponse]


class AllUsersEntryStatusesResponse(NamedTuple):
    users: list[UserEntryStatusResponse]

    def serialize(self) -> SerializedAllUsersEntryStatusesResponse:
        serialized_entry_statuses = []

        for user in self.users:
            serialized_entry_statuses.append(user.serialize())

        return SerializedAllUsersEntryStatusesResponse(users=serialized_entry_statuses)
