# -*- coding: utf-8 -*-
import fitz

print('=== PORTADA SIL ===')
pdf = fitz.open(r'contratos\SIL_2025.pdf')
print(pdf[0].get_text())
print('\n=== PAGINA 29 SIL ===')
print(pdf[28].get_text()[:2000])
pdf.close()
