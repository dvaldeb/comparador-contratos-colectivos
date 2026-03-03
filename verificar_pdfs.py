# -*- coding: utf-8 -*-
import fitz
import os

contratos_dir = r'c:\Users\dvaldeb\pupy inteeligente\contratos'

print('=== VERIFICANDO CONTENIDO DE PDFs ===')
print()

for archivo in sorted(os.listdir(contratos_dir)):
    if not archivo.endswith('.pdf'):
        continue
    filepath = os.path.join(contratos_dir, archivo)
    pdf = fitz.open(filepath)
    
    # Extraer texto de varias paginas
    texto_total = ''
    for i, page in enumerate(pdf):
        texto_total += page.get_text()
    
    # Contar caracteres y buscar palabras clave
    tiene_aniversario = 'aniversario' in texto_total.lower()
    tiene_uniforme = 'uniforme' in texto_total.lower()
    tiene_beca = 'beca' in texto_total.lower()
    tiene_casino = 'casino' in texto_total.lower() or 'alimentaci' in texto_total.lower()
    
    print(f'{archivo}:')
    print(f'  Paginas: {len(pdf)}')
    print(f'  Caracteres extraidos: {len(texto_total)}')
    print(f'  Aniversario: {tiene_aniversario}')
    print(f'  Uniforme: {tiene_uniforme}')
    print(f'  Beca: {tiene_beca}')
    print(f'  Casino/Alimentacion: {tiene_casino}')
    print()
    
    pdf.close()
