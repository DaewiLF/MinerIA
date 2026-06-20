from app.ml.models.base import AnalysisModel
from app.ml.models.copper_model import copper_model
from app.ml.models.mineral_model import mineral_model


DEFAULT_MODEL_ID = "copper"

MODEL_REGISTRY: dict[str, AnalysisModel] = {
    copper_model.model_id: copper_model,
    mineral_model.model_id: mineral_model,
}


def get_analysis_model(model_id: str | None) -> AnalysisModel:
    selected_id = (model_id or DEFAULT_MODEL_ID).strip().lower()
    if selected_id not in MODEL_REGISTRY:
        available = ", ".join(MODEL_REGISTRY)
        raise KeyError(f"Modelo no soportado: {selected_id}. Disponibles: {available}")
    return MODEL_REGISTRY[selected_id]


def list_analysis_models() -> list[dict[str, str]]:
    return [model.info() for model in MODEL_REGISTRY.values()]
