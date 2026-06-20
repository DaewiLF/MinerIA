import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

from app.ml.models.base import ModelPrediction


BACKEND_DIR = Path(__file__).resolve().parents[3]


class MineralClassifier:
    model_id = "minerals"
    model_name = "MineralClassifier"
    description = "Modelo multiclase para identificar el mineral predominante."

    def __init__(
        self,
        model_path: str | Path | None = None,
        labels_path: str | Path | None = None,
    ):
        self.model_path = Path(model_path) if model_path else BACKEND_DIR / "model_data" / "mineria_model.keras"
        self.labels_path = Path(labels_path) if labels_path else BACKEND_DIR / "model_data" / "labels.json"
        self.model = None
        self.labels: list[str] = []
        self.img_height = 224
        self.img_width = 224

    def info(self) -> dict[str, str]:
        return {
            "id": self.model_id,
            "name": "Modelo minerales",
            "description": self.description,
        }

    def load_labels(self) -> list[str]:
        if not self.labels:
            self.labels = json.loads(self.labels_path.read_text(encoding="utf-8"))
        return self.labels

    def load_model(self) -> bool:
        try:
            self.load_labels()
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Modelo cargado: {self.model_path}")
            print(f"Arquitectura de salida: {self.model.output_shape}")
            return True
        except Exception as exc:
            print(f"Error cargando el modelo multiclase: {exc}")
            return False

    def preprocess_image(self, image_path: str) -> np.ndarray | None:
        try:
            image = Image.open(image_path).convert("RGB")
            image = image.resize((self.img_width, self.img_height))
            image_array = np.array(image).astype("float32")
            return np.expand_dims(image_array, axis=0)
        except Exception as exc:
            print(f"Error en preprocesamiento multiclase: {exc}")
            return None

    def analyze(self, image_path: str) -> ModelPrediction | None:
        if not self.model and not self.load_model():
            return None

        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return None

        labels = self.load_labels()
        prediction = self.model.predict(processed_image, verbose=0)[0]
        predicted_idx = int(np.argmax(prediction))
        mineral_label = labels[predicted_idx]
        confidence = float(prediction[predicted_idx])
        copper_probability = float(prediction[labels.index("copper")]) if "copper" in labels else 0.0
        result = "con_cobre" if mineral_label == "copper" else "sin_cobre"
        probabilities = {
            label: float(prediction[index])
            for index, label in enumerate(labels)
        }
        top_predictions = sorted(
            probabilities.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:5]

        return ModelPrediction(
            model_id=self.model_id,
            model_name=self.model_name,
            result=result,
            confidence=confidence,
            raw_label=mineral_label,
            probabilities=probabilities,
            metadata={
                "tipo_modelo": "multiclase_minerales",
                "mineral_predicho": mineral_label,
                "probabilidad_cobre": copper_probability,
                "top_predicciones": [
                    {"label": label, "confidence": value}
                    for label, value in top_predictions
                ],
            },
        )

    def predict(self, image_path: str) -> tuple[str | None, float | None]:
        prediction = self.analyze(image_path)
        if prediction is None:
            return None, None
        return prediction.raw_label, prediction.confidence


mineral_model = MineralClassifier()
