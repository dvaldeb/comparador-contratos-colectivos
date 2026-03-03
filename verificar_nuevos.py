# -*- coding: utf-8 -*-
import fitz

for pdf_path, nombre in [('contratos\\FENATRALID_2024.pdf', 'FENATRALID'), ('contratos\\FSA_2024.pdf', 'FSA')]:
    pdf = fitz.open(pdf_path)
    texto = pdf[0].get_text()
    print(f'{nombre}:')
    print(f'  Paginas: {len(pdf)}')
    print(f'  Caracteres pag 1: {len(texto)}')
    print(f'  Tiene texto: {"Si" if len(texto) > 100 else "No (escaneado)"}')
    if len(texto) > 100:
        print(f'  Preview: {texto[:300]}...')
    pdf.close()
    print()
