import json
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow import keras


def diagnose(model_path: str, image_path: str):
    print("=" * 60)
    print("DIAGNÓSTICO DEL MODELO DE COBRE")
    print("=" * 60)

    # 1. Cargar modelo
    print(f"\n[1] Cargando modelo: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print(f"  Input:  {model.input_shape}")
    print(f"  Output: {model.output_shape}")
    print(f"  Capas:  {len(model.layers)}")

    if hasattr(model, "summary"):
        print("\n  --- Arquitectura ---")
        model.summary()

    # 2. Cargar imagen
    print(f"\n[2] Cargando imagen: {image_path}")
    img = Image.open(image_path).convert("RGB")
    print(f"  Original size: {img.size}")
    img_resized = img.resize((224, 224))
    raw_array = np.array(img_resized)
    print(f"  Resized dtype: {raw_array.dtype}, min={raw_array.min()}, max={raw_array.max()}")

    # 3. Preprocessing TEST A: exactamente como el proyecto de referencia
    print("\n[3A] Preprocessing REFERENCE (astype float32, /255.0)")
    ref_batch = np.expand_dims(np.array(img_resized).astype("float32"), axis=0)
    ref_processed = ref_batch / 255.0
    print(f"  dtype: {ref_processed.dtype}, min={ref_processed.min():.6f}, max={ref_processed.max():.6f}")

    # 3B. Preprocessing como estaba ANTES (float64)
    print("\n[3B] Preprocessing OLD (uint8 / 255.0 => float64)")
    old_batch = np.expand_dims(np.array(img_resized) / 255.0, axis=0)
    print(f"  dtype: {old_batch.dtype}, min={old_batch.min():.6f}, max={old_batch.max():.6f}")

    # 4. Predicción con ambos preprocessings
    print("\n[4] Predicciones:")
    for label, batch in [("REFERENCE (float32)", ref_processed), ("OLD (float64)", old_batch)]:
        pred = model(batch, training=False)
        pred_np = pred.numpy()
        print(f"\n  --- {label} ---")
        print(f"  Output shape: {pred_np.shape}")
        print(f"  Raw output: {pred_np}")

        if pred_np.shape[1] == 1:
            raw_val = float(pred_np[0][0])
            copper_p = 1.0 - raw_val
            print(f"  Modo INVERTIDO (1 - raw):")
            print(f"    raw={raw_val:.6f}, copper={copper_p:.6f}")
            if copper_p >= 0.5:
                print(f"    => con_cobre ({copper_p*100:.2f}%)")
            else:
                sin_p = 1.0 - copper_p
                print(f"    => sin_cobre ({sin_p*100:.2f}%)")
            print(f"  Modo NORMAL (raw = copper):")
            if raw_val >= 0.5:
                print(f"    => con_cobre ({raw_val*100:.2f}%)")
            else:
                print(f"    => sin_cobre ({(1-raw_val)*100:.2f}%)")
        elif pred_np.shape[1] == 2:
            best = int(np.argmax(pred_np[0]))
            print(f"  Modelo 2-neuronas, argmax={best}")
            print(f"    => {['sin_cobre', 'con_cobre'][best] if best < 2 else 'desconocido'}")
        else:
            print(f"  Output inesperado: {pred_np.shape}")

        del pred

    # 5. Verificar dtype del modelo
    print(f"\n[5] Pesos del modelo - dtype check:")
    for w in model.weights[:2]:
        print(f"  {w.name}: dtype={w.dtype}, shape={w.shape}")

    print("\n[6] Exportar predicción a JSON para comparar:")
    print(json.dumps({
        "procesamiento_usado": "float32 + /255.0",
        "raw_output": float(model(ref_processed, training=False).numpy()[0][0]),
    }, indent=2))

    print("\n" + "=" * 60)
    print("FIN DEL DIAGNÓSTICO")
    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit(
            "Uso: python diagnose_copper.py <ruta_modelo.h5> <ruta_imagen.jpg>\n"
            "Ej: docker exec mineria_backend python /app/diagnose_copper.py "
            "/app/model_data/model_copper_fixed.h5 /app/uploads/<imagen>.jpg"
        )
    diagnose(sys.argv[1], sys.argv[2])
