import pytesseract
from utils import preprocess_image

def run_ocr(image_path, lang="spa"):
    """
    Ejecuta el OCR sobre una imagen preprocesada.
    """
    processed_image = preprocess_image(image_path)

    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, lang=lang, config=config)

    return text
