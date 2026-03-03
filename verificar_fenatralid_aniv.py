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

# Retroceder para encontrar "Una vez al año"
inicio = idx_aniv
for i in range(idx_aniv, max(0, idx_aniv-100), -1):
    if texto_lower[i:i+10] == 'una vez al':
        inicio = i
        break

print(f'Inicio: {inicio}')

texto_desde = texto_limpio[inicio:]
match = re.search(r'cena\.', texto_desde.lower())
if match:
    fin = match.end()
else:
    fin = 400

clausula = texto_desde[:fin].strip()
print(f'\n=== CLAUSULA FENATRALID ({len(clausula)} chars) ===')
print(clausula)

pdf.close()
