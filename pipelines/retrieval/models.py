from dataclasses import dataclass
from typing import Dict


@dataclass
class RetrievalResult:
    chunk_id: str
    content: str
    score: float
    metadata: Dict