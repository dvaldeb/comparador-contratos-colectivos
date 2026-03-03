# -*- coding: utf-8 -*-
import fitz
import os
import re

contratos_dir = r'c:\Users\dvaldeb\pupy inteeligente\contratos'

# Palabras clave por tema
temas = {
    'Aniversarios': ['aniversario', 'años de servicio', 'quinquenio', 'antiguedad'],
    'Excelencia Academica': ['excelencia acad', 'beca', 'becas', 'escolaridad', 'rendimiento escolar'],
    'Uniformes': ['uniforme', 'uniformes', 'vestuario', 'vestimenta', 'ropa de trabajo'],
    'Casino': ['casino', 'alimentación', 'colación', 'bono alimentaci', 'comedor']
}

print('=' * 70)
print('ANALISIS DE CLAUSULAS POR CONTRATO COLECTIVO')
print('=' * 70)
print()

for archivo in sorted(os.listdir(contratos_dir)):
    if not archivo.endswith('.pdf'):
        continue
    
    sindicato = archivo.replace('.pdf', '').replace('_', ' ')
    filepath = os.path.join(contratos_dir, archivo)
    
    pdf = fitz.open(filepath)
    total_paginas = len(pdf)
    
    # Verificar si tiene texto
    texto_pag1 = pdf[0].get_text()
    es_escaneado = len(texto_pag1.strip()) < 100
    
    formato = 'ESCANEADO (imagen)' if es_escaneado else 'PDF con texto'
    
    print(f'### {sindicato.upper()} ###')
    print(f'Archivo: {archivo}')
    print(f'Total paginas: {total_paginas}')
    print(f'Formato: {formato}')
    print()
    
    if not es_escaneado:
        # Buscar paginas donde aparecen las clausulas
        for tema, keywords in temas.items():
            paginas_encontradas = []
            
            for page_num in range(total_paginas):
                page = pdf[page_num]
                texto = page.get_text().lower()
                
                for kw in keywords:
                    if kw.lower() in texto:
                        # Extraer contexto
                        idx = texto.find(kw.lower())
                        contexto = texto[max(0, idx-50):idx+100].replace('\n', ' ')
                        
                        if page_num + 1 not in [p[0] for p in paginas_encontradas]:
                            paginas_encontradas.append((page_num + 1, contexto[:80]))
                        break
            
            if paginas_encontradas:
                print(f'  {tema}:')
                for pag, ctx in paginas_encontradas[:3]:  # Max 3 paginas por tema
                    print(f'    - Pagina {pag}: "...{ctx}..."')
            else:
                print(f'  {tema}: No encontrado')
        print()
    else:
        print('  [No se puede buscar texto en PDF escaneado]')
        print('  Sugerencia: Revisar indice en paginas 1-3')
        print()
    
    pdf.close()
    print('-' * 70)
    print()
