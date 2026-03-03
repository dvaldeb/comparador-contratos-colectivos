# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf')

print('=== BUSCANDO TITULOS DE SECCIONES EN SIL ===')

for page_num in [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]:
    if page_num < len(pdf):
        page = pdf[page_num]
        texto = page.get_text()
        
        print(f'\n--- PAGINA {page_num + 1} ---')
        # Buscar líneas que parecen títulos (número + texto en mayúscula)
        lineas = texto.split('\n')
        for linea in lineas[:30]:
            linea_strip = linea.strip()
            if linea_strip and (linea_strip[0].isdigit() or any(kw in linea_strip.upper() for kw in ['BECA', 'CASINO', 'UNIFORME', 'ROPA', 'ALIMENTA'])):
                print(f'  {linea_strip[:80]}')

pdf.close()
