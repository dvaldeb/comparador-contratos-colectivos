# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\SIL_2025.pdf')

print('=== PAGINA 17 - BECAS SIL ===')
print(pdf[16].get_text())

print('\n\n=== PAGINA 18 - CONTINUACION ===')
print(pdf[17].get_text())

pdf.close()
