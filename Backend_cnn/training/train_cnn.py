import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os
import matplotlib.pyplot as plt

# === CONFIGURACIÓN ===
BASE_DIR = "C:/Users/patri/Escritorio/MinerIA_cnn/dataset"
MODEL_PATH = "C:/Users/patri/Escritorio/MinerIA_cnn/model_data/model_copper.h5"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 25

print("✅ TensorFlow version:", tf.__version__)

# === 1️⃣ Verificar dataset ===
print("🔍 Verificando estructura de dataset...")
con_cobre_path = os.path.join(BASE_DIR, "con_cobre")
sin_cobre_path = os.path.join(BASE_DIR, "sin_cobre")

if not os.path.exists(con_cobre_path):
    print(f"❌ ERROR: No existe {con_cobre_path}")
    exit()
if not os.path.exists(sin_cobre_path):
    print(f"❌ ERROR: No existe {sin_cobre_path}")
    exit()

num_con_cobre = len([f for f in os.listdir(con_cobre_path) if f.endswith(('.jpg', '.png', '.jpeg'))])
num_sin_cobre = len([f for f in os.listdir(sin_cobre_path) if f.endswith(('.jpg', '.png', '.jpeg'))])

print(f"📊 Imágenes 'con cobre': {num_con_cobre}")
print(f"📊 Imágenes 'sin cobre': {num_sin_cobre}")

# === 2️⃣ Generadores de imágenes ===
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=25,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2]
)

print("🔄 Cargando imágenes...")
train_gen = train_datagen.flow_from_directory(
    BASE_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset="training"
)

val_gen = train_datagen.flow_from_directory(
    BASE_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset="validation"
)

print(f"🎯 Clases detectadas: {train_gen.class_indices}")

# === 3️⃣ Modelo con MobileNetV2 ===
print("🧠 Cargando MobileNetV2...")
base_model = tf.keras.applications.MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)  # Formato explícito
)

# Congelar capas base
base_model.trainable = True
for layer in base_model.layers[:100]:
    layer.trainable = False

# === 4️⃣ Modelo completo ===
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# === 5️⃣ Compilar ===
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✅ Modelo compilado")
print(f"🚀 Iniciando entrenamiento ({EPOCHS} épocas)...")

# === 6️⃣ Entrenar ===
history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen,
    verbose=1
)

# === 7️⃣ Guardar ===
print("💾 Guardando modelo...")
model.save(MODEL_PATH)
print(f"✅ Modelo guardado en: {MODEL_PATH}")

# === 8️⃣ Gráficas ===
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Entrenamiento')
plt.plot(history.history['val_accuracy'], label='Validación')
plt.title('Precisión del Modelo')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Entrenamiento')
plt.plot(history.history['val_loss'], label='Validación')
plt.title('Pérdida del Modelo')
plt.legend()

plt.tight_layout()
plt.savefig('C:/Users/patri/Escritorio/MinerIA_cnn/model_data/training_plot.png')
print("📊 Gráficas guardadas")

# Resultados finales
final_val_acc = history.history['val_accuracy'][-1]
print(f"🎯 Precisión final en validación: {final_val_acc:.2%}")