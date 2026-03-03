# -*- coding: utf-8 -*-
import fitz
import re

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

pdf = fitz.open(r'contratos\SIL_2025.pdf')

texto = pdf[16].get_text() + '\n' + pdf[17].get_text() + '\n' + pdf[18].get_text()
texto_norm = normalizar(texto.upper())

# Buscar BECAS
idx = texto_norm.find('BECAS ESCOLARES')
for i in range(idx, max(0, idx-20), -1):
    if texto[i].isdigit():
        inicio = i
        num_clausula = int(texto[i])
        break

texto_desde = texto[inicio:]
print(f'Clausula inicio: {num_clausula}')

# Buscar siguiente clausula mayor
patron = r'\n\s*(\d+)[.\-\)]\s+[A-Z]'
for match in re.finditer(patron, texto_desde[50:]):
    num = int(match.group(1))
    if num > num_clausula:
        fin = match.start() + 50
        print(f'Fin encontrado: clausula {num} en pos {fin}')
        print(f'\nTexto extraido ({fin} chars):')
        print(texto_desde[:fin])
        break

pdf.close()
