# training/train_cnn_fixed_v2.py
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.regularizers import l2
import os
import matplotlib.pyplot as plt
import numpy as np

print("🔧 ENTRENAMIENTO MEJORADO V2 - SOLUCIÓN COMPLETA")

# Configuración
BASE_DIR = "C:/Users/patri/Escritorio/MinerIA_cnn/dataset"
MODEL_PATH = "C:/Users/patri/Escritorio/MinerIA_cnn/model_data/model_copper_fixed.h5"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 26

# === 1. LIMPIAR CACHE DE TENSORFLOW ===
tf.keras.backend.clear_session()

# === 2. DATA AUGMENTATION MÁS AGRESIVO ===
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=40,
    width_shift_range=0.4,
    height_shift_range=0.4,
    shear_range=0.3,
    zoom_range=0.4,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.5, 1.5],
    channel_shift_range=0.2,
    fill_mode='nearest'
)

# Datos de validación SIN aumento
val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_gen = train_datagen.flow_from_directory(
    BASE_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training',
    shuffle=True
)

val_gen = val_datagen.flow_from_directory(
    BASE_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation',
    shuffle=False
)

print(f"🎯 Clases: {train_gen.class_indices}")

# === 3. MODELO MÁS SIMPLE CON MÁS REGULARIZACIÓN ===
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)

# CONGELAR COMPLETAMENTE el modelo base inicialmente
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.6),  # Dropout muy alto
    layers.Dense(32, activation='relu', kernel_regularizer=l2(0.01)),  # Menas neuronas, más regularización
    layers.Dropout(0.4),
    layers.Dense(1, activation='sigmoid')
])

# === 4. COMPILAR CON LEARNING RATE MUY BAJO ===
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("🚀 FASE 1: Entrenando capas superiores...")
history1 = model.fit(
    train_gen,
    epochs=13,
    validation_data=val_gen,
    verbose=1
)

# === 5. FINE-TUNING: DESCONGELAR ALGUNAS CAPAS ===
base_model.trainable = True
for layer in base_model.layers[:120]:
    layer.trainable = False

# Recompilar con learning rate más bajo
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("🚀 FASE 2: Fine-tuning...")
history2 = model.fit(
    train_gen,
    epochs=13,
    validation_data=val_gen,
    verbose=1
)

# Combinar historiales
history = {
    'accuracy': history1.history['accuracy'] + history2.history['accuracy'],
    'val_accuracy': history1.history['val_accuracy'] + history2.history['val_accuracy'],
    'loss': history1.history['loss'] + history2.history['loss'],
    'val_loss': history1.history['val_loss'] + history2.history['val_loss']
}

# === 6. GUARDAR Y EVALUAR ===
model.save(MODEL_PATH)
print(f"💾 Modelo guardado en: {MODEL_PATH}")

# Evaluación final
val_loss, val_accuracy = model.evaluate(val_gen, verbose=0)
print(f"🎯 EVALUACIÓN FINAL:")
print(f"   - Precisión validación: {val_accuracy:.2%}")
print(f"   - Pérdida validación: {val_loss:.4f}")

# Probar con datos dummy para verificar que no siempre da 0.99
dummy_test = np.random.random((5, 224, 224, 3))
predictions = model.predict(dummy_test, verbose=0)
print(f"🔍 Prueba con datos aleatorios: {predictions.flatten()}")

# Gráficas
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history['accuracy'], label='Entrenamiento')
plt.plot(history['val_accuracy'], label='Validación')
plt.title('Precisión - Modelo Corregido')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history['loss'], label='Entrenamiento')
plt.plot(history['val_loss'], label='Validación')
plt.title('Pérdida - Modelo Corregido')
plt.legend()

plt.savefig('model_data/training_plot_fixed.png')
print("📊 Gráficas guardadas")