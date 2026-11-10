from dataclasses import dataclass, field

@dataclass
class SearchResult:
    algorithm: str
    found: bool
    path: list
    distance: float
    explored: list = field(default_factory=list)
    execution_time: float = 0.0