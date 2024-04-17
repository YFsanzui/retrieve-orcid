from dataclasses import dataclass

@dataclass
class Work:
    doi: str
    title: str
    created_at: str
    journal: str
    authors: str