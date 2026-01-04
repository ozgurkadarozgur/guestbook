from dataclasses import dataclass

@dataclass(frozen=True)
class UserDTO:
    id: int
    name: str
