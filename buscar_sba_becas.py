# -*- coding: utf-8 -*-
import fitz

pdfs = [
    ('contratos\\SIL_2025.pdf', 'SIL'),
    ('contratos\\FED_WM_2025.pdf', 'FED WM'),
    ('contratos\\FENATRALID_2024.pdf', 'FENATRALID'),
    ('contratos\\FSA_2024.pdf', 'FSA')
]

print('=== BUSCANDO SBA/ACUENTA EN EXCELENCIA ACADEMICA ===')
print()

for pdf_path, nombre in pdfs:
    print(f'\n{"="*50}')
    print(f'{nombre}')
    print(f'{"="*50}')
    
    pdf = fitz.open(pdf_path)
    
    for page_num in range(len(pdf)):
        texto = pdf[page_num].get_text()
        texto_lower = texto.lower()
        
        # Buscar páginas con becas/excelencia Y sba/acuenta/superbodega
        tiene_becas = 'beca' in texto_lower or 'excelencia' in texto_lower
        tiene_sba = 'sba' in texto_lower or 'superbodega' in texto_lower or 'acuenta' in texto_lower
        
        if tiene_becas and tiene_sba:
            print(f'\nPAGINA {page_num + 1} - Tiene BECAS + SBA/ACUENTA')
            # Mostrar contexto
            lineas = texto.split('\n')
            for i, linea in enumerate(lineas):
                if 'sba' in linea.lower() or 'superbodega' in linea.lower() or 'acuenta' in linea.lower():
                    inicio = max(0, i-2)
                    fin = min(len(lineas), i+5)
                    for j in range(inicio, fin):
                        print(f'  {lineas[j][:80]}')
                    print('  ...')
                    break
    
    pdf.close()

print('\n\n=== VERIFICANDO MARCAS EN PORTADAS ===')
for pdf_path, nombre in pdfs:
    pdf = fitz.open(pdf_path)
    texto_portada = pdf[0].get_text().lower()
    
    marcas = []
    if 'hiper' in texto_portada: marcas.append('Hiper')
    if 'express' in texto_portada: marcas.append('Express')
    if 'ekono' in texto_portada or 'econ' in texto_portada: marcas.append('Express 400')
    if 'sba' in texto_portada or 'superbodega' in texto_portada: marcas.append('SBA')
    if 'acuenta' in texto_portada: marcas.append('Acuenta')
    if 'mayorista' in texto_portada: marcas.append('Mayorista')
    
    print(f'{nombre}: {marcas}')
    pdf.close()
