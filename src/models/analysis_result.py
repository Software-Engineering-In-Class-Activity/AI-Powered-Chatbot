# AnalysisResult: simple container for NLP output (intent, entities, confidence).
from typing import Dict, Any, Optional


class AnalysisResult:
    # Holds the intent string, any extracted entities, and a confidence score.

    def __init__(self, intent: str = "", entities: Optional[Dict[str, Any]] = None, 
                 confidence: float = 0.0):
        # intent: identified intent; entities: dict of extracted values; confidence: 0.0-1.0
        self.intent: str = intent
        self.entities: Dict[str, Any] = entities if entities is not None else {}
        self.confidence: float = confidence
