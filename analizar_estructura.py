# -*- coding: utf-8 -*-
import fitz
import re

print('='*70)
print('ANALISIS COMPLETO DE ESTRUCTURA DE CONTRATOS')
print('='*70)

pdfs = [
    ('contratos\\SIL_2025.pdf', 'SIL'),
    ('contratos\\FED_WM_2025.pdf', 'FED WM'),
    ('contratos\\FENATRALID_2024.pdf', 'FENATRALID'),
    ('contratos\\FSA_2024.pdf', 'FSA')
]

for pdf_path, nombre in pdfs:
    print(f'\n{"="*70}')
    print(f'{nombre}')
    print(f'{"="*70}')
    
    pdf = fitz.open(pdf_path)
    
    # Buscar TÍTULOS de secciones (empresas)
    print('\n--- TITULOS/SECCIONES POR EMPRESA ---')
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        lineas = texto.split('\n')
        
        for linea in lineas:
            linea_upper = linea.upper().strip()
            # Buscar títulos que indican empresa específica
            if 'TÍTULO' in linea_upper or 'TITULO' in linea_upper:
                if any(emp in linea_upper for emp in ['HIPER', 'EXPRESS', 'EKONO', 'ECONÓMICOS', 'SBA', 'SUPERBODEGA', 'ACUENTA', 'MAYORISTA', 'ABARROTES']):
                    print(f'  Pag {i+1}: {linea.strip()[:80]}')
            # También buscar encabezados de capítulos
            elif linea_upper.startswith('CAP') or linea_upper.startswith('SECCI'):
                if any(emp in linea_upper for emp in ['HIPER', 'EXPRESS', 'EKONO', 'SBA', 'SUPERBODEGA', 'ACUENTA', 'MAYORISTA']):
                    print(f'  Pag {i+1}: {linea.strip()[:80]}')
    
    # Buscar las 4 cláusulas para cada empresa
    print('\n--- CLAUSULAS POR TEMA Y EMPRESA ---')
    
    clausulas_buscar = ['BECA', 'ANIVERSARIO', 'CASINO', 'ALIMENTACI', 'UNIFORME', 'ROPA DE TRABAJO', 'ROPA E IMPLEMENTOS']
    
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        texto_lower = texto.lower()
        
        for clausula in clausulas_buscar:
            if clausula.lower() in texto_lower:
                # Identificar qué empresa aplica en esta página
                empresas = []
                if 'hiper' in texto_lower: empresas.append('Hiper')
                if 'express' in texto_lower and '400' not in texto_lower: empresas.append('Express')
                if 'ekono' in texto_lower or 'económicos' in texto_lower or 'abarrotes econ' in texto_lower: empresas.append('Express400')
                if 'sba' in texto_lower or 'superbodega' in texto_lower: empresas.append('SBA')
                if 'acuenta' in texto_lower: empresas.append('Acuenta')
                if 'mayorista' in texto_lower: empresas.append('Mayorista')
                
                # Buscar el título de la cláusula
                for linea in texto.split('\n'):
                    linea_strip = linea.strip()
                    if clausula.lower() in linea_strip.lower() and len(linea_strip) < 100:
                        if linea_strip[0:3].replace('.','').replace('-','').strip().isdigit() or clausula.upper() in linea_strip.upper():
                            if empresas:
                                print(f'  Pag {i+1} [{"|".join(empresas)}]: {linea_strip[:70]}')
                            break
                break
    
    pdf.close()
