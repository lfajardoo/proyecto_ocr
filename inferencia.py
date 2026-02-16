#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
inferencia.py
Script CLI para aplicar el OCR a:
- una imagen
- una carpeta de imágenes

Opciones:
- imprimir por consola
- guardar en .txt
"""

import argparse
from pathlib import Path

from ocr_pipeline import OCRPipeline, OCRConfig, list_images


def save_text(out_dir: Path, img_path: Path, text: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{img_path.stem}.txt"
    out_file.write_text(text + "\n", encoding="utf-8")
    return out_file


def main():
    parser = argparse.ArgumentParser(description="OCR de páginas de libros (EasyOCR).")
    parser.add_argument("input", type=str, help="Ruta a imagen o carpeta con imágenes.")
    parser.add_argument("--langs", type=str, default="es,en", help="Idiomas separados por coma. Default: es,en")
    parser.add_argument("--gpu", action="store_true", help="Usar GPU (si está disponible en Torch/CUDA).")
    parser.add_argument("--preprocess", action="store_true", help="Aplicar preprocesamiento (recomendado).")
    parser.add_argument("--scale", type=float, default=1.5, help="Escalado del preprocesamiento. Default: 1.5")
    parser.add_argument("--denoise", action="store_true", help="Aplicar denoise (recomendado en fotos).")
    parser.add_argument("--min-conf", type=float, default=0.0, help="Filtrar texto con confianza menor a este valor.")
    parser.add_argument("--print", dest="print_console", action="store_true", help="Imprimir texto por consola.")
    parser.add_argument("--save-txt", action="store_true", help="Guardar salida en archivos .txt.")
    parser.add_argument("--out-dir", type=str, default="outputs", help="Carpeta de salida para .txt. Default: outputs")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    images = list_images(input_path)

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    if not langs:
        raise ValueError("Debes especificar al menos un idioma en --langs")

    config = OCRConfig(
        langs=langs,
        gpu=args.gpu,
        preprocess=args.preprocess,
        scale=args.scale,
        denoise=args.denoise,
        min_confidence=args.min_conf,
        paragraph=True,
        detail=1
    )

    pipeline = OCRPipeline(config)

    out_dir = Path(args.out_dir).expanduser().resolve()

    for img in images:
        out = pipeline.run_on_image(img)
        text = out["text"] if out["text"] else "[Sin texto detectado]"

        if args.print_console:
            print("\n" + "=" * 80)
            print(f"ARCHIVO: {out['path']}")
            print("-" * 80)
            print(text)
            print("=" * 80)

        if args.save_txt:
            saved = save_text(out_dir, img, out["text"])
            print(f"[OK] Guardado: {saved}")

    if not args.print_console and not args.save_txt:
        print("Nada que hacer: usa --print y/o --save-txt.")


if __name__ == "__main__":
    main()