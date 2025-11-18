import cv2
import numpy as np

def enhance_image(img):
    """Aplica un suavizado para mejorar contraste."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.equalizeHist(gray)
