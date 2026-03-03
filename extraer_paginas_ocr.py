# -*- coding: utf-8 -*-
import fitz
import os
import base64
import json

# Este script extrae páginas de los PDFs escaneados como imágenes
# para poder analizarlas con un modelo de visión

contratos_dir = r'c:\Users\dvaldeb\pupy inteeligente\contratos'
output_dir = r'c:\Users\dvaldeb\pupy inteeligente\paginas_ocr'
os.makedirs(output_dir, exist_ok=True)

pdfs_escaneados = ['Fed_Autonoma.pdf', 'Fenatralid.pdf', 'SIL.pdf']

# Palabras clave para buscar en títulos de sección
keywords_titulo = ['aniversario', 'beca', 'uniforme', 'casino', 'alimentaci', 'vestuario', 'excelencia']

print('=== EXTRAYENDO PAGINAS DE PDFs ESCANEADOS ===')
print()

for pdf_name in pdfs_escaneados:
    filepath = os.path.join(contratos_dir, pdf_name)
    sindicato = pdf_name.replace('.pdf', '')
    
    print(f'Procesando: {sindicato}')
    
    pdf = fitz.open(filepath)
    
    # Extraer algunas páginas representativas
    # (inicio, mitad, y algunas aleatorias)
    total_pages = len(pdf)
    pages_to_extract = [
        0,  # Portada
        1,  # Indice
        2,  # Inicio contenido
        int(total_pages * 0.25),  # 25%
        int(total_pages * 0.5),   # 50%
        int(total_pages * 0.75),  # 75%
        total_pages - 2,  # Penultima
    ]
    
    # Remover duplicados y ordenar
    pages_to_extract = sorted(set([p for p in pages_to_extract if 0 <= p < total_pages]))
    
    print(f'  Total paginas: {total_pages}')
    print(f'  Extrayendo paginas: {pages_to_extract}')
    
    for page_num in pages_to_extract:
        page = pdf[page_num]
        
        # Renderizar a imagen
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        img_path = os.path.join(output_dir, f'{sindicato}_pag{page_num+1:03d}.png')
        pix.save(img_path)
        print(f'    Guardada: {img_path}')
    
    pdf.close()
    print()

print('=== EXTRACCION COMPLETADA ===')
print(f'Imagenes guardadas en: {output_dir}')
print()
print('Ahora puedes revisar las imlmente o usar un modelo de visión.')
