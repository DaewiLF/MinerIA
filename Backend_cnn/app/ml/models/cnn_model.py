import tensorflow as tf
import numpy as np
from PIL import Image

class CopperCNN:
    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None
        self.img_height = 224
        self.img_width = 224
        # ACTUALIZADO: El nuevo modelo usa binary classification
        self.class_names = {0: 'sin_cobre', 1: 'con_cobre'}
        
    def load_model(self):
        """Cargar modelo pre-entrenado"""
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            print("✅ Modelo cargado exitosamente")
            print(f"🔍 Arquitectura de salida: {self.model.output_shape}")
            return True
        except Exception as e:
            print(f"❌ Error cargando el modelo: {e}")
            return False
    
    def preprocess_image(self, image_path):
        """Preprocesar imagen para predicción - ACTUALIZADO"""
        try:
            # Cargar y redimensionar imagen
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize((self.img_width, self.img_height))
            
            # Convertir a array y normalizar
            img_array = np.array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"❌ Error en preprocesamiento: {e}")
            return None
    
    def predict(self, image_path):
        """Realizar predicción - COMPLETAMENTE ACTUALIZADO"""
        if not self.model:
            if not self.load_model():
                return None, None
        
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return None, None
        
        # Obtener predicción
        prediction = self.model.predict(processed_image, verbose=0)
        
        print(f"🔍 Predicción cruda: {prediction}")  # Debug
        
        # PARA MODELO BINARIO (1 neurona sigmoid)
        if prediction.shape[1] == 1:
            probability = float(prediction[0][0])
            
            print(f"🧪 Probabilidad sigmoid: {probability}")

            if probability > 0.5:
                predicted_class = 'sin_cobre'  # ACTUALIZADO: Invertido para compatibilidad con nuevo modelo
                confidence = probability
            else:
                predicted_class = 'con_cobre' 
                confidence = 1 - probability

        # PARA MODELO MULTICLASE (2 neuronas softmax) - compatibilidad
        else:
            predicted_idx = np.argmax(prediction[0])
            confidence = float(prediction[0][predicted_idx])
            predicted_class = self.class_names.get(predicted_idx, 'desconocido')
        
        print(f"🎯 Clase: {predicted_class}, Confianza: {confidence:.2%}")
        return predicted_class, float(confidence)

# Instancia global del modelo
copper_model = CopperCNN('model_data/model_copper_fixed.h5')