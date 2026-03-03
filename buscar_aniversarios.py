# -*- coding: utf-8 -*-
import fitz

for pdf_path, nombre in [(r'contratos\SIL_2025.pdf', 'SIL'), (r'contratos\FED_WM_2025.pdf', 'FED WM')]:
    print(f'\n{"="*60}')
    print(f'{nombre} - ANIVERSARIOS')
    print(f'{"="*60}')
    pdf = fitz.open(pdf_path)
    for i in range(len(pdf)):
        texto = pdf[i].get_text()
        if 'aniversario' in texto.lower():
            print(f'\n--- PAGINA {i+1} ---')
            # Mostrar contexto
            lineas = texto.split('\n')
            for j, linea in enumerate(lineas):
                if 'aniversario' in linea.lower():
                    # Mostrar 3 lineas antes y 5 despues
                    inicio = max(0, j-2)
                    fin = min(len(lineas), j+8)
                    for k in range(inicio, fin):
                        print(f'  {lineas[k][:90]}')
                    print('  ...')
                    break
    pdf.close()
