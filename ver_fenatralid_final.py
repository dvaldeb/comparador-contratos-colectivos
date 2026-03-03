# -*- coding: utf-8 -*-
import fitz
import re

pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')
texto = pdf[39].get_text() + '\n' + pdf[40].get_text()

# Normalizar
texto_limpio = re.sub(r'\s+', ' ', texto)
texto_lower = texto_limpio.lower()

idx_aniv = texto_lower.find('aniversario')
texto_antes = texto_lower[max(0, idx_aniv-100):idx_aniv]
idx_una = texto_antes.find('una vez')
if idx_una != -1:
    inicio = max(0, idx_aniv-100) + idx_una
else:
    inicio = idx_aniv

texto_desde = texto_limpio[inicio:]
match = re.search(r'cena\.', texto_desde.lower())
fin = match.end() if match else 400

clausula = texto_desde[:fin].strip()
print(f'=== FENATRALID ANIVERSARIO ({len(clausula)} chars) ===')
print(clausula)

pdf.close()
