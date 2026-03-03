# -*- coding: utf-8 -*-
import fitz

print('='*70)
print('REVISION DE CLAUSULAS DE ANIVERSARIO')
print('='*70)

docs = [
    ('SIL', r'contratos\SIL_2025.pdf', 26),
    ('FED WM', r'contratos\FED_WM_2025.pdf', 11),
    ('FENATRALID', r'contratos\FENATRALID_2024.pdf', 40),
    ('FSA', r'contratos\FSA_2024.pdf', 21)
]

for nombre, path, pag in docs:
    print(f'\n{"="*50}')
    print(f'{nombre} - Página {pag}')
    print(f'{"="*50}')
    
    pdf = fitz.open(path)
    texto = pdf[pag-1].get_text()
    
    # Buscar "aniversario" en el texto
    texto_lower = texto.lower()
    if 'aniversario' in texto_lower:
        idx = texto_lower.find('aniversario')
        # Mostrar contexto amplio
        inicio = max(0, idx - 200)
        fin = min(len(texto), idx + 500)
        print(texto[inicio:fin])
    else:
        print('NO ENCONTRADO en esta página')
    
    pdf.close()
