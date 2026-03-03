# -*- coding: utf-8 -*-
import fitz

print('='*70)
print('FED WM - ESTRUCTURA DETALLADA')
print('='*70)

pdf = fitz.open(r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf')

# Ver páginas clave
paginas_clave = [6, 14, 34, 45, 50, 55]

for pag in paginas_clave:
    print(f'\n{"="*50}')
    print(f'PAGINA {pag}')
    print(f'{"="*50}')
    texto = pdf[pag-1].get_text()[:1500]
    print(texto)

pdf.close()
