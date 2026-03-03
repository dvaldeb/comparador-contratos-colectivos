# -*- coding: utf-8 -*-
import fitz

print('=== BUSCANDO SBA/ACUENTA EN SIL - DETALLE ===')

pdf = fitz.open(r'contratos\SIL_2025.pdf')

for i in range(len(pdf)):
    texto = pdf[i].get_text()
    texto_lower = texto.lower()
    
    if 'sba' in texto_lower or 'acuenta' in texto_lower:
        print(f'\nPAGINA {i+1}:')
        for linea in texto.split('\n'):
            if 'sba' in linea.lower() or 'acuenta' in linea.lower():
                print(f'  {linea.strip()[:80]}')

pdf.close()
