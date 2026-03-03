# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\SIL_2025.pdf')

print('=== PAGINA 26 - ANIVERSARIO SIL ===')
print(pdf[25].get_text())

print('\n=== PAGINA 27 ===')
print(pdf[26].get_text()[:2000])

pdf.close()
