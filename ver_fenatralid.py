# -*- coding: utf-8 -*-
import fitz

print('='*70)
print('FENATRALID - ESTRUCTURA DETALLADA')
print('='*70)

pdf = fitz.open(r'c:\Users\dvaldeb\pupy inteeligente\contratos\FENATRALID_2024.pdf')

# Ver páginas clave
paginas_clave = [19, 43, 54, 59, 62]

for pag in paginas_clave:
    print(f'\n{"="*50}')
    print(f'PAGINA {pag}')
    print(f'{"="*50}')
    texto = pdf[pag-1].get_text()[:1800]
    print(texto)

pdf.close()
