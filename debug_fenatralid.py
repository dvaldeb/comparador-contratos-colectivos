# -*- coding: utf-8 -*-
import fitz
import re

pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')
texto = pdf[39].get_text() + '\n' + pdf[40].get_text()

# Normalizar
texto_limpio = re.sub(r'\n\s*', ' ', texto)
texto_lower = texto_limpio.lower()

idx_aniv = texto_lower.find('aniversario')
print(f'Aniversario en pos: {idx_aniv}')
print(f'\n100 chars ANTES de aniversario:')
print(texto_limpio[idx_aniv-100:idx_aniv])

# Buscar "una vez" en todo el texto
idx_una = texto_lower.find('una vez al')
print(f'\n"Una vez al" en pos: {idx_una}')
print(f'Distancia: {idx_aniv - idx_una} chars')

pdf.close()
