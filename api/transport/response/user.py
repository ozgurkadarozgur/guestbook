from typing import TypedDict, NamedTuple


class SerializedUserResponse(TypedDict):
    name: str


class UserResponse(NamedTuple):
    name: str

    def serialize(self) -> SerializedUserResponse:
        return SerializedUserResponse(
            name=self.name,
        )
