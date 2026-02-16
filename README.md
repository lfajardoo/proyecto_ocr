# proyecto_ocr

## 1. Descripción de la tarea
Este repositorio implementa un OCR reproducible en Python para extraer texto desde imágenes. Poyecto_ocr aplicaciones ML 2026-1 Urosario.
Se apoya en **EasyOCR** (modelos preentrenados) y contiene:
- `ocr_pipeline.py`: pipeline principal (carga modelo, preprocesa y ejecuta OCR).
- `inferencia.py`: script de inferencia (CLI) para procesar una imagen o carpeta.

## 2. Requisitos del sistema
- Python 3.9+ (recomendado 3.10+)
- Linux / macOS / Windows
- RAM: 4GB+ (recomendado)
- Opcional: GPU con CUDA si deseas acelerar (Torch/CUDA configurado)

## 3. Instrucciones de instalación
```bash
git clone <TU_REPO_URL>
cd ocr-libros

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt
