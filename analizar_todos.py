# -*- coding: utf-8 -*-
import fitz
import re

print('='*70)
print('ANALISIS DETALLADO DE ESTRUCTURA POR FORMATO')
print('='*70)

pdfs = [
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf', 'FED WM'),
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\FENATRALID_2024.pdf', 'FENATRALID'),
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\FSA_2024.pdf', 'FSA')
]

for pdf_path, nombre in pdfs:
    print(f'\n{"="*70}')
    print(f'{nombre}')
    print(f'{"="*70}')
    
    pdf = fitz.open(pdf_path)
    
    # 1. Buscar TITULOS de secciones por empresa
    print('\n1. SECCIONES/TITULOS POR EMPRESA:')
    for i in range(min(len(pdf), 80)):
        texto = pdf[i].get_text()
        lineas = texto.split('\n')
        
        for linea in lineas:
            linea_strip = linea.strip()
            linea_upper = linea_strip.upper()
            
            if len(linea_strip) > 20:
                # Buscar titulos de secciones
                if any(x in linea_upper for x in ['TITULO', 'TÍTULO', 'CLAUSULAS APLICABLES', 'CLÁUSULAS APLICABLES', 'CAPITULO', 'CAPÍTULO']):
                    print(f'  Pag {i+1}: {linea_strip[:80]}')
                # Buscar menciones de empresas en encabezados
                elif any(x in linea_upper for x in ['HIPER LTDA', 'EXPRESS LTDA', 'EKONO', 'ABARROTES', 'MAYORISTA', 'ACUENTA', 'SBA']):
                    if any(y in linea_upper for y in ['PARA', 'APLICABLE', 'TRABAJADORES DE', 'EXCLUSIVAMENTE']):
                        print(f'  Pag {i+1}: {linea_strip[:80]}')
    
    # 2. Buscar clausulas de BECAS por pagina
    print('\n2. CLAUSULAS DE BECAS (por formato):')
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        texto_lower = texto.lower()
        
        if 'beca' in texto_lower and 'rosita' not in texto_lower:
            # Identificar formato de esta seccion
            formatos = []
            if 'hiper' in texto_lower: formatos.append('Hiper')
            if 'express' in texto_lower and '400' not in texto_lower: formatos.append('Express')
            if 'ekono' in texto_lower or 'econ' in texto_lower: formatos.append('Express400')
            if 'sba' in texto_lower or 'superbodega' in texto_lower: formatos.append('SBA')
            if 'acuenta' in texto_lower: formatos.append('Acuenta')
            if 'mayorista' in texto_lower: formatos.append('Mayorista')
            
            for linea in texto.split('\n'):
                if 'beca' in linea.lower() and 'escolar' in linea.lower():
                    if len(linea.strip()) < 80:
                        print(f'  Pag {i+1} {formatos}: {linea.strip()}')
                        break
    
    # 3. Buscar clausulas de CASINO por pagina
    print('\n3. CLAUSULAS DE CASINO (por formato):')
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        texto_lower = texto.lower()
        
        if 'casino' in texto_lower:
            formatos = []
            if 'hiper' in texto_lower: formatos.append('Hiper')
            if 'express' in texto_lower: formatos.append('Express')
            if 'ekono' in texto_lower: formatos.append('Express400')
            if 'sba' in texto_lower: formatos.append('SBA')
            if 'acuenta' in texto_lower: formatos.append('Acuenta')
            if 'mayorista' in texto_lower: formatos.append('Mayorista')
            
            for linea in texto.split('\n'):
                linea_upper = linea.upper().strip()
                if 'CASINO' in linea_upper and ('ALIMENTA' in linea_upper or linea_upper[0].isdigit()):
                    if len(linea.strip()) < 80:
                        print(f'  Pag {i+1} {formatos}: {linea.strip()}')
                        break
    
    # 4. Buscar clausulas de UNIFORMES/ROPA por pagina
    print('\n4. CLAUSULAS DE UNIFORMES/ROPA (por formato):')
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        texto_lower = texto.lower()
        
        if 'ropa' in texto_lower or 'uniforme' in texto_lower:
            formatos = []
            if 'hiper' in texto_lower: formatos.append('Hiper')
            if 'express' in texto_lower: formatos.append('Express')
            if 'ekono' in texto_lower: formatos.append('Express400')
            if 'sba' in texto_lower: formatos.append('SBA')
            if 'acuenta' in texto_lower: formatos.append('Acuenta')
            if 'mayorista' in texto_lower: formatos.append('Mayorista')
            
            for linea in texto.split('\n'):
                linea_upper = linea.upper().strip()
                if ('ROPA' in linea_upper or 'UNIFORME' in linea_upper) and 'TRABAJO' in linea_upper:
                    if linea_upper[0].isdigit() and len(linea.strip()) < 80:
                        print(f'  Pag {i+1} {formatos}: {linea.strip()}')
                        break
    
    # 5. Buscar ANIVERSARIO
    print('\n5. CLAUSULAS DE ANIVERSARIO (por formato):')
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        texto_lower = texto.lower()
        
        if 'aniversario' in texto_lower:
            formatos = []
            if 'hiper' in texto_lower: formatos.append('Hiper')
            if 'express' in texto_lower: formatos.append('Express')
            if 'ekono' in texto_lower: formatos.append('Express400')
            if 'sba' in texto_lower: formatos.append('SBA')
            if 'acuenta' in texto_lower: formatos.append('Acuenta')
            if 'mayorista' in texto_lower: formatos.append('Mayorista')
            
            for linea in texto.split('\n'):
                if 'aniversario' in linea.lower():
                    print(f'  Pag {i+1} {formatos}: {linea.strip()[:70]}')
                    break
    
    pdf.close()
