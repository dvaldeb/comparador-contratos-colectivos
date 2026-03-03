# -*- coding: utf-8 -*-
import fitz
import re

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')

texto = pdf[42].get_text() + '\n' + pdf[43].get_text() + '\n' + pdf[44].get_text()
texto_norm = normalizar(texto.upper())

# Buscar inicio
idx = texto_norm.find('BECAS')
for i in range(idx, max(0, idx-20), -1):
    if texto[i].isdigit():
        inicio = i
        break

texto_desde = texto[inicio:]
texto_norm_desde = normalizar(texto_desde.upper())

# Buscar PRESTAMO
match = re.search(r'\d+\.\d+[.\s]+PRESTAMO', texto_norm_desde)
if match:
    fin = match.start()
    print(f'Fin en PRESTAMO pos {fin}')
    print(f'\nUltimas 200 chars de BECAS (sin prestamo):')
    print(texto_desde[fin-200:fin])

pdf.close()
