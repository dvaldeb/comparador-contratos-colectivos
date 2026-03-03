# -*- coding: utf-8 -*-
import fitz
import re

print('=== BUSCANDO CLAUSULA EXCELENCIA ACADEMICA ===')
print()

pdfs = [
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf', 'SIL'),
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf', 'FED WM')
]

for pdf_path, nombre in pdfs:
    print(f'\n{"="*60}')
    print(f'{nombre}')
    print(f'{"="*60}')
    
    pdf = fitz.open(pdf_path)
    
    # Buscar páginas con "excelencia" o "beca"
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_lower = texto.lower()
        
        if 'excelencia acad' in texto_lower or 'becas escolares' in texto_lower:
            print(f'\n--- PÁGINA {page_num + 1} ---')
            
            # Mostrar las líneas que contienen excelencia o beca
            lineas = texto.split('\n')
            for i, linea in enumerate(lineas):
                if 'excelencia' in linea.lower() or 'beca' in linea.lower():
                    # Mostrar contexto (5 líneas antes y 20 después)
                    inicio = max(0, i-3)
                    fin = min(len(lineas), i+25)
                    contexto = '\n'.join(lineas[inicio:fin])
                    print(contexto)
                    print('\n[...]\n')
                    break
    
    pdf.close()
