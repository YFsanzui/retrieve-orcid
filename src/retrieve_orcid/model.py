from dataclasses import dataclass

@dataclass
class Work:
    doi: str
    title: str
    created_at: str
    published_day: str
    journal: str
    authors: str