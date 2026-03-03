# -*- coding: utf-8 -*-
import fitz

print('=== FED WM - PAGINA 11 ===')
pdf = fitz.open(r'contratos\FED_WM_2025.pdf')
print(pdf[10].get_text()[:2500])
pdf.close()

print('\n\n=== FENATRALID - PAGINA 40 ===')
pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')
print(pdf[39].get_text()[:2500])
pdf.close()
