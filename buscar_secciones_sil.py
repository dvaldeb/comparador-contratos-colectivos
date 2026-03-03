# -*- coding: utf-8 -*-
import fitz

print('=== BUSCANDO SECCIONES POR EMPRESA EN SIL ===')

pdf = fitz.open(r'contratos\SIL_2025.pdf')

for i in range(len(pdf)):
    texto = pdf[i].get_text()
    lineas = texto.split('\n')
    
    for linea in lineas[:15]:  # Solo las primeras 15 líneas de cada página
        linea_upper = linea.upper().strip()
        # Buscar líneas que parecen encabezados de sección
        if any(x in linea_upper for x in ['CL\u00c1USULAS APLICABLES', 'CLAUSULAS APLICABLES', 'T\u00cdTULO', 'TITULO', 
                                           'ADMINISTRADORA DE SUPERMERCADOS', 'ABARROTES ECON', 'WALMART CHILE MAYORISTA',
                                           'TRABAJADORES DE', 'PARA LOS TRABAJADORES']):
            if len(linea.strip()) > 20:
                print(f'Pag {i+1}: {linea.strip()[:100]}')

pdf.close()
