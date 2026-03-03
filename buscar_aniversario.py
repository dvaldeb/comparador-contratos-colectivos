# -*- coding: utf-8 -*-
import fitz

print('=== Buscando ANIVERSARIO en cada documento ===')

docs = [
    ('SIL', r'contratos\SIL_2025.pdf'),
    ('FED WM', r'contratos\FED_WM_2025.pdf'),
    ('FENATRALID', r'contratos\FENATRALID_2024.pdf'),
    ('FSA', r'contratos\FSA_2024.pdf')
]

for nombre, path in docs:
    print(f'\n{nombre}:')
    pdf = fitz.open(path)
    encontrado = False
    for i in range(len(pdf)):
        texto = pdf[i].get_text().lower()
        if 'aniversario' in texto:
            print(f'  Pagina {i+1}: SI')
            encontrado = True
    if not encontrado:
        print(f'  NO ENCONTRADO')
    pdf.close()
