# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\SIL_2025.pdf')

print('=== ESTRUCTURA DEL SIL - EMPRESAS Y BECAS ===')
print()

# Buscar títulos de empresas/secciones
for i in range(len(pdf)):
    texto = pdf[i].get_text()
    texto_lower = texto.lower()
    
    # Buscar menciones de empresas con becas
    if 'beca' in texto_lower:
        empresas = []
        if 'sba' in texto_lower or 'superbodega' in texto_lower:
            empresas.append('SBA')
        if 'acuenta' in texto_lower:
            empresas.append('Acuenta')
        if 'hiper' in texto_lower:
            empresas.append('Hiper')
        if 'express' in texto_lower and 'express 400' not in texto_lower:
            empresas.append('Express')
        if 'ekono' in texto_lower or 'econ' in texto_lower:
            empresas.append('Ekono/Express400')
        if 'mayorista' in texto_lower:
            empresas.append('Mayorista')
        
        if empresas:
            print(f'PAG {i+1}: BECAS para {empresas}')
            # Mostrar el título de la sección
            for linea in texto.split('\n'):
                if 'beca' in linea.lower() and len(linea.strip()) < 100:
                    print(f'  -> {linea.strip()}')
                    break

pdf.close()
