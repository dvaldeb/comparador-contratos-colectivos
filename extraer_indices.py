# -*- coding: utf-8 -*-
import fitz
import os
import base64

contratos_dir = r'c:\Users\dvaldeb\pupy inteeligente\contratos'
output_dir = r'c:\Users\dvaldeb\pupy inteeligente\indices_ocr'
os.makedirs(output_dir, exist_ok=True)

pdfs_escaneados = ['Fed_Autonoma.pdf', 'Fenatralid.pdf', 'SIL.pdf']

print('=== EXTRAYENDO INDICES DE PDFs ESCANEADOS ===')
print()

for pdf_name in pdfs_escaneados:
    filepath = os.path.join(contratos_dir, pdf_name)
    sindicato = pdf_name.replace('.pdf', '')
    
    print(f'Procesando: {sindicato}')
    
    pdf = fitz.open(filepath)
    
    # Extraer primeras 5 paginas (donde suele estar el indice)
    for page_num in range(min(5, len(pdf))):
        page = pdf[page_num]
        
        # Renderizar a imagen de alta calidad
        zoom = 2.5
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        img_path = os.path.join(output_dir, f'{sindicato}_pag{page_num+1:02d}.png')
        pix.save(img_path)
        print(f'  Guardada: pag{page_num+1}')
    
    pdf.close()
    print()

print('Imagenes guardadas en:', output_dir)
print()
print('Archivos creados:')
for f in sorted(os.listdir(output_dir)):
    print(f'  {f}')
