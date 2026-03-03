# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')

# Revisar las páginas de cada tema
print('=== FENATRALID - Excelencia Académica (Pág 43-44-45) ===')
for p in [42, 43, 44]:
    print(f'\n--- PÁGINA {p+1} ---')
    print(pdf[p].get_text())

pdf.close()
