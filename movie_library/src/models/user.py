from dataclasses import dataclass, field

@dataclass
class User:
    user_Id: str
    email: str
    password: str
    movies: list[str] = field(default_factory=list)