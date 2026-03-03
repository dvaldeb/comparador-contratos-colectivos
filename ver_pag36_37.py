# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\SIL_2025.pdf')

print('=== PAGINA 36 SIL ===')
print(pdf[35].get_text()[:2500])

print('\n=== PAGINA 37 SIL (BECAS SBA) ===')
print(pdf[36].get_text())

pdf.close()
