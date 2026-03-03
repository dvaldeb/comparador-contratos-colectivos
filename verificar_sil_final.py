# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\SIL_2025.pdf')
texto = pdf[16].get_text() + pdf[17].get_text()

idx = texto.upper().find('BECAS ESCOLARES')
for i in range(idx, max(0, idx-20), -1):
    if texto[i].isdigit():
        inicio = i
        break

becas = texto[inicio:inicio+1670]
print('=== ULTIMAS 400 CHARS DE BECAS SIL ===')
print(becas[-400:])

if 'CUMPLEA' in becas.upper():
    print('\n*** ERROR: CUMPLEANIOS INCLUIDO ***')
else:
    print('\n*** OK: NO INCLUYE CUMPLEANIOS ***')

pdf.close()
