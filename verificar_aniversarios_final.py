# -*- coding: utf-8 -*-
import fitz
import re

print('=== VERIFICACION ANIVERSARIOS ===')

docs = [
    ('SIL', r'contratos\SIL_2025.pdf', 26),
    ('FED WM', r'contratos\FED_WM_2025.pdf', 11),
    ('FENATRALID', r'contratos\FENATRALID_2024.pdf', 40),
    ('FSA', r'contratos\FSA_2024.pdf', 21)
]

for nombre, path, pag in docs:
    pdf = fitz.open(path)
    texto = pdf[pag-1].get_text() + '\n' + pdf[pag].get_text()
    texto_lower = texto.lower()
    
    idx_aniv = texto_lower.find('aniversario')
    if idx_aniv == -1:
        print(f'{nombre}: NO ENCONTRADO')
        continue
    
    # Retroceder para encontrar "Una vez al año"
    inicio = idx_aniv
    for i in range(idx_aniv, max(0, idx_aniv-150), -1):
        if texto_lower[i:i+10] == 'una vez al':
            inicio = i
            break
    
    texto_desde = texto[inicio:]
    
    # Buscar fin
    fin = len(texto_desde)
    patrones_fin = [r'cena\.\s', r'correspondiere\.']
    for patron in patrones_fin:
        match = re.search(patron, texto_desde.lower())
        if match:
            fin = match.end()
            break
    
    if fin > 600:
        fin = 600
    
    clausula = texto_desde[:fin].strip()
    clausula = re.sub(r'\n\s+', ' ', clausula)
    
    print(f'\n{nombre} ({len(clausula)} chars):')
    print(clausula)
    print('-'*50)
    
    pdf.close()
