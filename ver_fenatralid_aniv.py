# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'contratos\FENATRALID_2024.pdf')
texto = pdf[39].get_text()

print('=== FENATRALID PAG 40 ===')
idx = texto.lower().find('aniversario')
print(f'Aniversario en pos: {idx}')
print(f'\nTexto ANTES (400 chars):')
print(texto[max(0,idx-400):idx])
print(f'\n--- ANIVERSARIO ---')
print(texto[idx:idx+500])

pdf.close()
