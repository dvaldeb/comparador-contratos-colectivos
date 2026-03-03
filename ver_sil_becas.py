# -*- coding: utf-8 -*-
import fitz
import re

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

pdf = fitz.open(r'contratos\SIL_2025.pdf')

texto = pdf[16].get_text() + '\n' + pdf[17].get_text() + '\n' + pdf[18].get_text()

# Buscar BECAS
idx = texto.upper().find('BECAS ESCOLARES')
for i in range(idx, max(0, idx-20), -1):
    if texto[i].isdigit():
        inicio = i
        break

texto_desde = texto[inicio:]
print(f'Longitud texto desde BECAS: {len(texto_desde)}')
print('\n=== TEXTO EXTRAIDO (primeros 2500 chars) ===')
print(texto_desde[:2500])

pdf.close()
