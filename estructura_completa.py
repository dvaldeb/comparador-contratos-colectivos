# -*- coding: utf-8 -*-
import fitz

print('='*70)
print('ESTRUCTURA COMPLETA DE TODOS LOS CONTRATOS')
print('='*70)

# Mapeo de empresas legales a marcas comerciales
print('''
MAPEO DE EMPRESAS LEGALES A MARCAS:
- Administradora de Supermercados Hiper Ltda. -> HIPER
- Administradora de Supermercados Express Ltda. -> EXPRESS  
- Abarrotes Economicos Ltda. -> SBA, ACUENTA
- Ekono Ltda. -> EXPRESS 400 (ex Ekono)
- Walmart Chile Mayorista Ltda. -> MAYORISTA
''')

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
    
    # Buscar secciones/titulos por empresa
    print('\nSECCIONES POR EMPRESA:')
    
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        lineas = texto.split('\n')
        
        for linea in lineas:
            linea_strip = linea.strip()
            linea_upper = linea_strip.upper()
            
            # Buscar titulos de secciones
            if ('TITULO' in linea_upper or 'CLAUSULAS APLICABLES' in linea_upper) and len(linea_strip) > 30:
                print(f'  Pag {i+1}: {linea_strip[:75]}')
    
    # Buscar las 4 clausulas y a que empresa aplican
    print('\nCLAUSULAS (Becas, Casino, Uniformes, Aniversario):')
    
    clausulas_encontradas = []
    
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        texto_lower = texto.lower()
        
        # Identificar empresa de esta seccion
        empresas = []
        if 'hiper' in texto_lower and 'express' in texto_lower:
            empresas = ['Hiper', 'Express']
        elif 'abarrotes econ' in texto_lower or ('sba' in texto_lower and 'acuenta' not in texto_lower):
            empresas = ['SBA/Acuenta']
        elif 'ekono' in texto_lower:
            empresas = ['Express400']
        elif 'mayorista' in texto_lower:
            empresas = ['Mayorista']
        
        # Buscar clausulas
        for linea in texto.split('\n'):
            linea_upper = linea.upper().strip()
            
            if 'BECA' in linea_upper and ('ESCOLARES' in linea_upper or linea_upper.startswith(('1','2','3','4','5','6','7','8','9'))):
                if 'ROSITA' not in linea_upper:  # Excluir Beca Rosita Pineda
                    key = f'Becas-{i+1}'
                    if key not in clausulas_encontradas:
                        print(f'  Pag {i+1} [Becas] {empresas}: {linea.strip()[:50]}')
                        clausulas_encontradas.append(key)
            
            if ('CASINO' in linea_upper or 'ALIMENTACION' in linea_upper) and linea_upper.startswith(('1','2','3','4','5','6','7','8','9')):
                key = f'Casino-{i+1}'
                if key not in clausulas_encontradas:
                    print(f'  Pag {i+1} [Casino] {empresas}: {linea.strip()[:50]}')
                    clausulas_encontradas.append(key)
            
            if ('ROPA' in linea_upper or 'UNIFORME' in linea_upper) and ('TRABAJO' in linea_upper or 'IMPLEMENTOS' in linea_upper):
                if linea_upper.startswith(('1','2','3','4','5','6','7','8','9')):
                    key = f'Uniforme-{i+1}'
                    if key not in clausulas_encontradas:
                        print(f'  Pag {i+1} [Uniformes] {empresas}: {linea.strip()[:50]}')
                        clausulas_encontradas.append(key)
            
            if 'ANIVERSARIO' in linea_upper:
                key = f'Aniversario-{i+1}'
                if key not in clausulas_encontradas:
                    print(f'  Pag {i+1} [Aniversario] {empresas}: {linea.strip()[:50]}')
                    clausulas_encontradas.append(key)
    
    pdf.close()
