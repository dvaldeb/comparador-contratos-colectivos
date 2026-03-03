# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\FED_WM_2025.pdf')

print('=== FED WM - PAGINA 11 COMPLETA ===')
print(pdf[10].get_text())

print('\n=== FED WM - PAGINA 12 ===')
print(pdf[11].get_text()[:2000])

pdf.close()
