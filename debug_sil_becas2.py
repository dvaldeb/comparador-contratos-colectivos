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
        num_clausula = int(texto[i])
        break

texto_desde = texto[inicio:]
print(f'Clausula inicio: {num_clausula}')
print(f'Longitud texto: {len(texto_desde)}')

# Buscar CUMPLEAÑOS
if 'CUMPLEA' in texto_desde.upper():
    idx_cump = texto_desde.upper().find('CUMPLEA')
    print(f'CUMPLEA encontrado en pos: {idx_cump}')
    print(f'Contexto: {texto_desde[idx_cump-30:idx_cump+50]}')

# Buscar patron de clausula 9
patron = r'9[.\-\):]\s*CUMPLEA'
match = re.search(patron, texto_desde.upper())
if match:
    print(f'\nPatron 9.- CUMPLEA encontrado en pos: {match.start()}')
    fin = match.start()
    print(f'\nTexto SOLO BECAS ({fin} chars):')
    print(texto_desde[:fin])

pdf.close()
