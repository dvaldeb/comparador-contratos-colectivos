# -*- coding: utf-8 -*-
import fitz

print('=== BUSCANDO MARCAS EN LOS CONTRATOS ===')
print()

pdfs = [
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf', 'SIL'),
    (r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf', 'FED WM')
]

marcas_buscar = ['hiper', 'express', 'superbodega', 'sba', 'ekono', 'acuenta', 'líder', 'lider', 
                 'central', 'distribución', 'bodega', 'walmart', 'tienda', 'local', 'establecimiento']

for pdf_path, nombre in pdfs:
    print(f'=== {nombre} ===')
    pdf = fitz.open(pdf_path)
    
    # Revisar primeras 5 páginas para encontrar menciones de marcas
    marcas_encontradas = {}
    
    for page_num in range(min(10, len(pdf))):
        page = pdf[page_num]
        texto = page.get_text().lower()
        
        for marca in marcas_buscar:
            if marca in texto:
                if marca not in marcas_encontradas:
                    marcas_encontradas[marca] = []
                if page_num + 1 not in marcas_encontradas[marca]:
                    marcas_encontradas[marca].append(page_num + 1)
    
    print('Marcas/formatos mencionados:')
    for marca, paginas in marcas_encontradas.items():
        print(f'  {marca}: páginas {paginas}')
    
    # Mostrar texto de página 1 para ver el encabezado
    print()
    print('Primeras líneas del contrato:')
    texto_pag1 = pdf[0].get_text()[:500]
    print(texto_pag1)
    print()
    print('-' * 50)
    
    pdf.close()
