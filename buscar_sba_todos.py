# -*- coding: utf-8 -*-
import fitz

print('=== BUSCANDO SBA/ACUENTA EN TODOS LOS DOCUMENTOS ===')

pdfs = [
    ('contratos\\SIL_2025.pdf', 'SIL'),
    ('contratos\\FED_WM_2025.pdf', 'FED WM'),
    ('contratos\\FENATRALID_2024.pdf', 'FENATRALID'),
    ('contratos\\FSA_2024.pdf', 'FSA')
]

for pdf_path, nombre in pdfs:
    print(f'\n{"="*50}')
    print(f'{nombre}')
    print(f'{"="*50}')
    
    pdf = fitz.open(pdf_path)
    
    # Ver portada
    portada = pdf[0].get_text()
    print('EMPRESAS EN PORTADA:')
    for linea in portada.split('\n'):
        linea_strip = linea.strip()
        if 'LTDA' in linea_strip.upper() or 'LIMITADA' in linea_strip.upper():
            print(f'  {linea_strip[:70]}')
    
    # Buscar SBA/Acuenta/SuperBodega
    tiene_sba = False
    tiene_acuenta = False
    for i in range(len(pdf)):
        texto = pdf[i].get_text().lower()
        if 'sba' in texto or 'superbodega' in texto or 'super bodega' in texto:
            if not tiene_sba:
                print(f'\n  [SI] Tiene SBA/SuperBodega')
                tiene_sba = True
        if 'acuenta' in texto:
            if not tiene_acuenta:
                print(f'  [SI] Tiene Acuenta')
                tiene_acuenta = True
    
    if not tiene_sba and not tiene_acuenta:
        print('\n  [NO] NO tiene SBA ni Acuenta')
    
    pdf.close()
