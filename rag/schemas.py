from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Segment:
    start: float
    end: float
    text: str
    speaker: Optional[str] = None

@dataclass
class Chunk:
    episode_id: str
    text: str
    start: float
    end: float
    speakers: Optional[List[str]] = None
