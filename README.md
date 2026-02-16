<<<<<<< HEAD
# proyecto_ocr
proyecto_ocr aplicaciones ML 2026-1
=======
# Sistema OCR para Extracción de Texto desde Imágenes

## 1. Descripción General

Este proyecto implementa un sistema de Reconocimiento Óptico de Caracteres (OCR) capaz de extraer texto desde imágenes de páginas de libros escaneadas o fotografiadas.

El sistema incluye:

- Preprocesamiento de imágenes con OpenCV
- Extracción de texto con Tesseract OCR
- Script de inferencia por línea de comandos
- Organización modular del código

---

## 2. Requisitos del Sistema

- Python 3.8+
- Tesseract OCR instalado en el sistema

### Instalar Tesseract (Linux)

```
sudo apt install tesseract-ocr
sudo apt install tesseract-ocr-spa
```

En Windows:
Descargar desde:
https://github.com/tesseract-ocr/tesseract

---

## 3. Instalación

1. Clonar el repositorio:

```
git clone <URL_DEL_REPOSITORIO>
cd proyecto_ocr
```

2. Crear entorno virtual:

```
python -m venv venv
source venv/bin/activate  # Linux
```

3. Instalar dependencias:

```
pip install pytesseract opencv-python numpy
```

---

## 4. Estructura del Proyecto

```
proyecto_ocr/
│
├── src/
│   ├── ocr_pipeline.py
│   ├── utils.py
│   └── inferencia.py
│
└── README.md
```

- ocr_pipeline.py → Ejecuta el OCR
- utils.py → Funciones de preprocesamiento
- inferencia.py → Script de inferencia
- README.md → Documentación del proyecto

---

## 5. Uso del Sistema

### Procesar una imagen:

```
python src/inferencia.py --imagen data/pagina1.jpg
```

### Procesar una imagen y guardar resultado:

```
python src/inferencia.py --imagen data/pagina1.jpg --output resultado.txt
```

### Procesar una carpeta completa:

```
python src/inferencia.py --carpeta data/
```

---

## 6. Ejemplo

Entrada:
Imagen de una página escaneada.

Salida:
Texto extraído mostrado en consola o guardado en archivo .txt.

---

## 7. Limitaciones y Mejoras Futuras

- Sensible a imágenes con mala iluminación.
- No incluye corrección ortográfica.
- Se puede mejorar agregando:
  - Corrección de inclinación (deskew)
  - Eliminación avanzada de ruido
  - Uso de modelos OCR más avanzados como EasyOCR o PaddleOCR

---

## Autor

Proyecto desarrollado como parte del Taller Práctico de OCR.
>>>>>>> master
