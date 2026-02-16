import argparse
import os
from ocr_pipeline import run_ocr

def process_single_image(image_path, output_file=None):
    text = run_ocr(image_path)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Texto guardado en {output_file}")
    else:
        print("\n===== TEXTO EXTRAÍDO =====\n")
        print(text)

def process_folder(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            full_path = os.path.join(folder_path, file)
            print(f"\nProcesando: {file}")
            process_single_image(full_path)

def main():
    parser = argparse.ArgumentParser(description="Sistema OCR para páginas de libros")

    parser.add_argument("--imagen", type=str, help="Ruta a una imagen")
    parser.add_argument("--carpeta", type=str, help="Ruta a carpeta de imágenes")
    parser.add_argument("--output", type=str, help="Archivo de salida opcional")

    args = parser.parse_args()

    if args.imagen:
        process_single_image(args.imagen, args.output)
    elif args.carpeta:
        process_folder(args.carpeta)
    else:
        print("Debe proporcionar --imagen o --carpeta")

if __name__ == "__main__":
    main()
