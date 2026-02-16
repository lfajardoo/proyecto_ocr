import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Preprocesa la imagen para mejorar el OCR:
    - Escala de grises
    - Reducción de ruido
    - Binarización adaptativa
    """
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"No se pudo cargar la imagen: {image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Reducir ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Binarización
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh
