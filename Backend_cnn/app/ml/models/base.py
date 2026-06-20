from dataclasses import dataclass, field
from typing import Any, Dict, Protocol


@dataclass
class ModelPrediction:
    model_id: str
    model_name: str
    result: str
    confidence: float
    raw_label: str
    probabilities: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class AnalysisModel(Protocol):
    model_id: str
    model_name: str
    description: str

    def analyze(self, image_path: str) -> ModelPrediction | None:
        ...

    def info(self) -> Dict[str, str]:
        ...
