# -*- coding: utf-8 -*-
import fitz

pdfs = [
    ('contratos\\SIL_2025.pdf', 'SIL'),
    ('contratos\\FED_WM_2025.pdf', 'FED WM'),
    ('contratos\\FENATRALID_2024.pdf', 'FENATRALID'),
    ('contratos\\FSA_2024.pdf', 'FSA')
]

print('=== BUSCANDO TERMINOS DE BECAS EN TODOS LOS DOCUMENTOS ===')
print()

for pdf_path, nombre in pdfs:
    print(f'\n{"="*60}')
    print(f'{nombre}')
    print(f'{"="*60}')
    
    pdf = fitz.open(pdf_path)
    
    for page_num in range(len(pdf)):
        texto = pdf[page_num].get_text()
        texto_lower = texto.lower()
        
        # Buscar cualquier mención de becas
        if 'beca' in texto_lower:
            # Buscar títulos de sección
            lineas = texto.split('\n')
            for linea in lineas:
                linea_upper = linea.upper().strip()
                # Buscar líneas que parecen títulos (con número o en mayúsculas)
                if 'BECA' in linea_upper and (linea_upper[0].isdigit() or linea_upper.startswith('BECA')):
                    print(f'  Pag {page_num + 1}: {linea.strip()[:70]}')
    
    pdf.close()
