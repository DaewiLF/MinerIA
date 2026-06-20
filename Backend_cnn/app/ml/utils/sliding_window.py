from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np


@dataclass(frozen=True)
class SlidingWindowPatch:
    """Un parche 224x224 y su ubicación original en la imagen macro.

    Coordenadas en formato (x_min, y_min, x_max, y_max), donde x_max/y_max son
    *exclusivos* (estilo slicing de NumPy): img[y_min:y_max, x_min:x_max].
    """

    patch: np.ndarray | None
    x_min: int
    y_min: int
    x_max: int
    y_max: int


def _compute_starts(total: int, window: int, stride: int) -> List[int]:
    """Devuelve los inicios (start) para una dimensión.

    Regla:
    - Avanza con `stride` mientras quepa el window.
    - Siempre incluye el último start ajustado (total - window) para cubrir borde.
    """

    if total <= window:
        return [0]

    starts = list(range(0, total - window + 1, stride))
    last = total - window
    if starts[-1] != last:
        starts.append(last)
    return starts


def sliding_window_patches(
    image: np.ndarray,
    *,
    patch_size: Tuple[int, int] = (224, 224),
    overlap: int = 32,
    pad_if_smaller: bool = True,
    return_patches: bool = True,
) -> List[SlidingWindowPatch]:
    """Segmenta una imagen panorámica en parches con ventana deslizante.

    Parámetros
    - image: np.ndarray (H,W) o (H,W,C)
    - patch_size: (alto, ancho). Por defecto 224x224.
    - overlap: traslape en píxeles. Por defecto 32.
      El stride queda: patch - overlap, por defecto 192.
    - pad_if_smaller: si la imagen es más pequeña que 224 en alguna dimensión,
      aplica padding por reflexión (sin negro) para poder extraer al menos 1 parche.

        Retorna
        - Lista de SlidingWindowPatch, cada uno con el patch (np.ndarray) y coordenadas
            (x_min, y_min, x_max, y_max) respecto a la imagen original.
        - Si return_patches=False, `patch` será None y solo se devuelve la grilla de
            coordenadas (útil para evitar uso de RAM en panoramas grandes).

    Notas de bordes
    - Si el tamaño no es múltiplo del stride, la última ventana de cada fila/columna
      se ajusta hacia atrás para mantener 224x224 sin deformar.
    """

    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("image debe ser un np.ndarray")

    if image.ndim not in (2, 3):
        raise ValueError("image debe tener forma (H,W) o (H,W,C)")

    patch_h, patch_w = patch_size
    if patch_h <= 0 or patch_w <= 0:
        raise ValueError("patch_size inválido")

    if overlap < 0:
        raise ValueError("overlap debe ser >= 0")

    stride_x = patch_w - overlap
    stride_y = patch_h - overlap
    if stride_x <= 0 or stride_y <= 0:
        raise ValueError("overlap no puede ser >= patch_size")

    orig_h, orig_w = image.shape[:2]

    # Si la imagen es más chica que el patch, hacemos padding por reflexión.
    # Mantenemos las coordenadas retornadas respecto a la imagen original:
    # como solo habrá un parche, sus coords serán (0,0,patch_w,patch_h) recortadas
    # a la imagen original para trazabilidad.
    padded = image
    pad_bottom = max(0, patch_h - orig_h)
    pad_right = max(0, patch_w - orig_w)
    if (pad_bottom > 0 or pad_right > 0) and pad_if_smaller:
        padded = cv2.copyMakeBorder(
            image,
            top=0,
            bottom=pad_bottom,
            left=0,
            right=pad_right,
            borderType=cv2.BORDER_REFLECT_101,
        )

    h, w = padded.shape[:2]

    x_starts = _compute_starts(w, patch_w, stride_x)
    y_starts = _compute_starts(h, patch_h, stride_y)

    patches: List[SlidingWindowPatch] = []

    for y in y_starts:
        for x in x_starts:
            x2 = x + patch_w
            y2 = y + patch_h
            patch: np.ndarray | None
            if return_patches:
                patch = padded[y:y2, x:x2]

                # Seguridad: asegurar tamaño exacto
                if patch.shape[0] != patch_h or patch.shape[1] != patch_w:
                    # No rellenamos con negro: si ocurre, es un bug de starts/bordes.
                    raise RuntimeError(
                        f"Patch no es {patch_h}x{patch_w}: got {patch.shape[:2]}"
                    )
            else:
                patch = None

            # Coordenadas respecto a la imagen original (clamp).
            # Si hubo padding, x2/y2 podrían exceder orig_w/orig_h.
            x_min = int(min(max(x, 0), orig_w))
            y_min = int(min(max(y, 0), orig_h))
            x_max = int(min(max(x2, 0), orig_w))
            y_max = int(min(max(y2, 0), orig_h))

            patches.append(
                SlidingWindowPatch(
                    patch=patch,
                    x_min=x_min,
                    y_min=y_min,
                    x_max=x_max,
                    y_max=y_max,
                )
            )

    return patches
