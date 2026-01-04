from dataclasses import dataclass


@dataclass(frozen=True)
class UserDTO:
    id: int
    name: str


@dataclass(frozen=True)
class UserEntryStatusDTO:
    name: str
    last_entry: str
    total_entry_count: int
