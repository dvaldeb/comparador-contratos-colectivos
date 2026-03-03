# -*- coding: utf-8 -*-
import fitz
import re

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')

# Simular extraccion de Becas pag 43
texto = pdf[42].get_text() + '\n' + pdf[43].get_text() + '\n' + pdf[44].get_text()
texto_norm = normalizar(texto.upper())

print(f'Total texto: {len(texto)} chars')

# Buscar inicio de BECAS
if 'BECAS' in texto_norm:
    idx = texto_norm.find('BECAS')
    print(f'BECAS encontrado en pos {idx}')
    
    # Retroceder para encontrar numero
    for i in range(idx, max(0, idx-20), -1):
        if texto[i].isdigit():
            inicio = i
            print(f'Numero encontrado en pos {inicio}: {texto[inicio:inicio+5]}')
            break
    
    texto_desde = texto[inicio:]
    print(f'Texto desde inicio: {len(texto_desde)} chars')
    
    # Buscar clausula 19
    patron_fin = r'\n\s*19[.\-\)]\s+[A-Z]'
    match_fin = re.search(patron_fin, texto_desde)
    if match_fin:
        fin = match_fin.start()
        print(f'Clausula 19 encontrada en pos {fin}')
        print(f'Longitud final: {fin} chars')
        print('\nUltimas 300 chars antes de clausula 19:')
        print(texto_desde[fin-300:fin])
    else:
        print('Clausula 19 NO encontrada')

pdf.close()
