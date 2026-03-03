# -*- coding: utf-8 -*-
import fitz
import re

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

pdf = fitz.open(r'contratos\SIL_2025.pdf')

# Simular extracción
texto = pdf[16].get_text() + "\n" + pdf[17].get_text() + "\n" + pdf[18].get_text()
texto_norm = normalizar(texto.upper())

# Buscar inicio
for kw in ['BECAS ESCOLARES']:
    kw_norm = normalizar(kw)
    patron = r'\d+[.\-\):\s]*' + re.escape(kw_norm)
    match = re.search(patron, texto_norm)
    if match:
        inicio = match.start()
        print(f'Inicio encontrado en posición: {inicio}')
        print(f'Texto inicio: {texto[inicio:inicio+100]}')
        break

texto_desde_inicio = texto[inicio:]
texto_norm_desde = normalizar(texto_desde_inicio.upper())

# Buscar fin
patron_fin = r'\d+[.\-\):\s]*(CUMPLEA|NACIMIENTO DE HIJO|BONO POR NACIMIENTO)'
match_fin = re.search(patron_fin, texto_norm_desde)
if match_fin:
    fin = match_fin.start()
    print(f'Fin encontrado en posición: {fin}')
    print(f'Texto fin: {texto_desde_inicio[fin:fin+50]}')
else:
    print('No se encontró fin')
    fin = len(texto_desde_inicio)

clausula = texto_desde_inicio[:fin].strip()
print(f'\nLongitud cláusula: {len(clausula)}')
print('\n=== CLAUSULA EXTRAIDA ===')
print(clausula)

pdf.close()
