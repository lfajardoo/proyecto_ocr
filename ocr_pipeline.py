#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ocr_pipeline.py
Pipeline principal para OCR de páginas de libros (escaneadas o fotografiadas).

Responsabilidades:
- Cargar/inicializar el modelo OCR (EasyOCR).
- Preprocesar imágenes (opcional, recomendado para fotos/escaneos).
- Ejecutar OCR y devolver texto + metadatos.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

import cv2
import easyocr


# Extensiones soportadas
EXTS_IMAGEN = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


@dataclass(frozen=True)
class OCRConfig:
    langs: List[str] = None              # e.g. ["es", "en"]
    gpu: bool = False
    preprocess: bool = True
    scale: float = 1.5                   # reescalado antes de umbral/adaptativo
    denoise: bool = True                 # reduce ruido
    paragraph: bool = True               # agrupa texto en párrafos (EasyOCR)
    detail: int = 1                      # 1 => (bbox, text, conf)
    min_confidence: float = 0.0          # filtra resultados con baja confianza

    def __post_init__(self):
        if self.langs is None:
            object.__setattr__(self, "langs", ["es", "en"])


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in EXTS_IMAGEN


def list_images(input_path: Path) -> List[Path]:
    """
    Devuelve lista de imágenes a procesar.
    - Si input_path es archivo: lo valida y devuelve [archivo]
    - Si es carpeta: busca recursivamente imágenes soportadas
    """
    if input_path.is_file():
        if not is_image_file(input_path):
            raise ValueError(f"Archivo no soportado o no es imagen: {input_path}")
        return [input_path]

    if input_path.is_dir():
        imgs = [p for p in sorted(input_path.rglob("*")) if is_image_file(p)]
        if not imgs:
            raise ValueError(f"No se encontraron imágenes en: {input_path}")
        return imgs

    raise ValueError(f"Ruta inválida: {input_path}")


def preprocess_image(img_bgr, scale: float = 1.5, denoise: bool = True):
    """
    Preprocesamiento típico para páginas:
    - reescalado (mejora OCR si la foto es pequeña)
    - grises
    - denoise
    - umbral adaptativo (robusto a sombras)
    """
    if scale and scale != 1.0:
        h, w = img_bgr.shape[:2]
        img_bgr = cv2.resize(
            img_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC
        )

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    if denoise:
        gray = cv2.fastNlMeansDenoising(gray, h=10)

    th = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 10
    )
    return th


class OCRPipeline:
    """
    Pipeline OCR reutilizable.
    Crea el reader una vez (costoso) y luego procesa múltiples imágenes.
    """

    def __init__(self, config: Optional[OCRConfig] = None):
        self.config = config or OCRConfig()
        self.reader = easyocr.Reader(self.config.langs, gpu=self.config.gpu)

    def run_on_image(self, image_path: Path) -> Dict[str, Any]:
        """
        Ejecuta OCR sobre una imagen.
        Retorna dict con:
        - path
        - text (str)
        - results (lista EasyOCR)
        """
        image_path = image_path.expanduser().resolve()
        img_bgr = cv2.imread(str(image_path))
        if img_bgr is None:
            raise ValueError(f"No se pudo leer la imagen: {image_path}")

        img_input = (
            preprocess_image(img_bgr, scale=self.config.scale, denoise=self.config.denoise)
            if self.config.preprocess
            else img_bgr
        )

        results = self.reader.readtext(
            img_input,
            detail=self.config.detail,
            paragraph=self.config.paragraph
        )

        # results típicamente: [(bbox, text, conf), ...]
        lines: List[str] = []
        filtered_results = []
        for r in results:
            if not r or len(r) < 2:
                continue
            text = r[1]
            conf = r[2] if len(r) >= 3 else 1.0
            if conf >= self.config.min_confidence:
                lines.append(text)
                filtered_results.append(r)

        text_out = "\n".join(lines).strip()

        return {
            "path": str(image_path),
            "text": text_out,
            "results": filtered_results,
        }
