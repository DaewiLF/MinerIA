from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image

from app.ml.models.base import ModelPrediction


BACKEND_DIR = Path(__file__).resolve().parents[3]


class CopperCNN:
    model_id = "copper"
    model_name = "CopperCNN"
    description = "Modelo binario especializado en detectar presencia de cobre."

    def __init__(self, model_path: str | Path | None = None):
        self.model_path = Path(model_path) if model_path else BACKEND_DIR / "model_data" / "model_copper_fixed.h5"
        self.model = None
        self.img_height = 224
        self.img_width = 224
        self.class_names = {0: "sin_cobre", 1: "con_cobre"}

    def info(self) -> dict[str, str]:
        return {
            "id": self.model_id,
            "name": "Modelo cobre",
            "description": self.description,
        }

    def load_model(self) -> bool:
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print(f"Modelo cargado: {self.model_path}")
            print(f"Arquitectura de salida: {self.model.output_shape}")
            return True
        except Exception as exc:
            print(f"Error cargando el modelo de cobre: {exc}")
            return False

    def preprocess_image(self, image_path: str) -> np.ndarray | None:
        try:
            image = Image.open(image_path).convert("RGB")
            image = image.resize((self.img_width, self.img_height))
            image_array = np.array(image) / 255.0
            return np.expand_dims(image_array, axis=0)
        except Exception as exc:
            print(f"Error en preprocesamiento de cobre: {exc}")
            return None

    def analyze(self, image_path: str) -> ModelPrediction | None:
        if not self.model and not self.load_model():
            return None

        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return None

        prediction = self.model.predict(processed_image, verbose=0)

        if prediction.shape[1] == 1:
            raw_probability = float(prediction[0][0])
            copper_probability = 1.0 - raw_probability
            if copper_probability >= 0.5:
                predicted_class = "con_cobre"
                confidence = copper_probability
            else:
                predicted_class = "sin_cobre"
                confidence = 1.0 - copper_probability
            probabilities = {
                "sin_cobre": float(1.0 - copper_probability),
                "con_cobre": float(copper_probability),
            }
        else:
            predicted_idx = int(np.argmax(prediction[0]))
            confidence = float(prediction[0][predicted_idx])
            predicted_class = self.class_names.get(predicted_idx, "desconocido")
            probabilities = {
                self.class_names.get(index, f"clase_{index}"): float(value)
                for index, value in enumerate(prediction[0])
            }

        return ModelPrediction(
            model_id=self.model_id,
            model_name=self.model_name,
            result=predicted_class,
            confidence=float(confidence),
            raw_label=predicted_class,
            probabilities=probabilities,
            metadata={"tipo_modelo": "binario_cobre"},
        )

    def predict(self, image_path: str) -> tuple[str | None, float | None]:
        prediction = self.analyze(image_path)
        if prediction is None:
            return None, None
        return prediction.result, prediction.confidence


copper_model = CopperCNN()
