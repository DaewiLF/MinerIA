import gc
import os
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow import keras


BACKEND_DIR = Path(__file__).resolve().parents[3]
GRADCAM_DIR = os.path.join(BACKEND_DIR, "uploads", "gradcam")


def cleanup_tf_memory(*objs) -> None:
    """Libera tensores y grafos de TF de la RAM.

    Parámetros
    ----------
    *objs : objetos TF a eliminar explícitamente antes del GC.
    """
    for obj in objs:
        if obj is not None:
            try:
                del obj
            except Exception:
                pass
    gc.collect()


def find_last_conv_layer(model: keras.Model) -> keras.layers.Layer:
    for layer in reversed(model.layers):
        if isinstance(layer, keras.Model):
            try:
                return find_last_conv_layer(layer)
            except ValueError:
                pass

        try:
            output = layer.output
        except AttributeError:
            continue

        if isinstance(output, (list, tuple)):
            output = output[0]

        shape = getattr(output, "shape", None)
        if shape is not None and len(shape) == 4:
            return layer

    raise ValueError("No se encontro una capa convolucional para Grad-CAM.")


def find_last_conv_with_parent(model: keras.Model) -> Tuple[keras.Model, keras.layers.Layer]:
    for layer in reversed(model.layers):
        if isinstance(layer, keras.Model):
            try:
                return find_last_conv_with_parent(layer)
            except ValueError:
                pass

        try:
            output = layer.output
        except AttributeError:
            continue

        if isinstance(output, (list, tuple)):
            output = output[0]

        shape = getattr(output, "shape", None)
        if shape is not None and len(shape) == 4:
            return model, layer

    raise ValueError("No se encontro una capa convolucional para Grad-CAM.")


def forward_with_capture(
    model: keras.Model,
    inputs: tf.Tensor,
    target_parent: keras.Model,
    target_layer: keras.layers.Layer,
) -> Tuple[tf.Tensor, tf.Tensor, keras.Model]:
    conv_outputs = None
    x = inputs
    feature_model = None

    for layer in model.layers:
        if layer is target_parent:
            feature_model = keras.Model(
                target_parent.inputs,
                [target_layer.output, target_parent.output],
            )
            conv_outputs, x = feature_model(x, training=False)
            continue

        try:
            x = layer(x, training=False)
        except TypeError:
            x = layer(x)

        if layer is target_layer:
            conv_outputs = x

    return conv_outputs, x, feature_model


def make_gradcam_heatmap(
    model: keras.Model,
    image_batch: np.ndarray,
    class_index: int,
    invert: bool = False,
) -> np.ndarray:
    target_parent, last_conv = find_last_conv_with_parent(model)

    processed = tf.constant(image_batch, dtype=tf.float32)
    model(processed, training=False)

    with tf.GradientTape() as tape:
        conv_outputs, predictions, feature_model = forward_with_capture(
            model, processed, target_parent, last_conv,
        )
        if conv_outputs is None:
            raise ValueError(f"No se pudo capturar la capa convolucional: {last_conv.name}")
        class_channel = -predictions[:, class_index] if invert else predictions[:, class_index]

    grads = tape.gradient(class_channel, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0)

    max_val = tf.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val

    result = heatmap.numpy()
    cleanup_tf_memory(feature_model, tape, grads, pooled_grads, conv_outputs, heatmap)
    return result


def _get_target_class_index(
    model_id: str,
    prediction_result: str,
    raw_label: str,
    model: keras.Model,
    labels: Optional[List[str]] = None,
) -> int:
    output_shape = model.output_shape
    num_outputs = output_shape[-1] if output_shape else 1

    if model_id == "minerals" and labels and num_outputs > 1:
        return labels.index(raw_label) if raw_label in labels else 0

    if model_id == "copper" and num_outputs > 1:
        return 1 if prediction_result == "con_cobre" else 0

    return 0


def save_gradcam_overlay(
    image_path: str,
    heatmap: np.ndarray,
    model_id: str,
    prediction_result: str = "unknown",
) -> str:
    original_bgr = cv2.imread(image_path)
    if original_bgr is None:
        original_rgb = cv2.cvtColor(
            np.array(Image.open(image_path).convert("RGB")),
            cv2.COLOR_RGB2BGR,
        )
    else:
        original_rgb = original_bgr

    heatmap_resized = cv2.resize(heatmap, (original_rgb.shape[1], original_rgb.shape[0]))
    heatmap_uint8 = np.uint8(255 * heatmap_resized)
    heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(original_rgb, 0.62, heatmap_colored, 0.38, 0)

    os.makedirs(GRADCAM_DIR, exist_ok=True)
    stem = Path(image_path).stem
    filename = f"gradcam_{model_id}_{stem}_{prediction_result}.jpg"
    output_path = os.path.join(GRADCAM_DIR, filename)
    cv2.imwrite(output_path, overlay)

    return f"/uploads/gradcam/{filename}"


def generate_gradcam(
    model: keras.Model,
    image_path: str,
    image_batch: np.ndarray,
    model_id: str,
    prediction_result: str,
    raw_label: str,
    labels: Optional[List[str]] = None,
) -> Tuple[str, np.ndarray]:
    class_index = _get_target_class_index(model_id, prediction_result, raw_label, model, labels)

    num_outputs = model.output_shape[-1] if model.output_shape else 1
    invert = model_id == "copper" and num_outputs == 1

    heatmap = make_gradcam_heatmap(model, image_batch, class_index, invert=invert)
    target_label = "con_cobre" if model_id == "copper" else prediction_result
    gradcam_url = save_gradcam_overlay(image_path, heatmap, model_id, target_label)
    return gradcam_url, heatmap
