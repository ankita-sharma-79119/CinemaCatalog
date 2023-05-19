from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Movie:
    movie_Id: str
    name: str
    director: str
    year: int
    writers: list[str] = field(default_factory=list)
    plot: str = None
    cast: list[str] = field(default_factory=list)
    last_watched: datetime = None
    rating: int = 0
    genres: list[str] = field(default_factory=list)
    video_link: str = None