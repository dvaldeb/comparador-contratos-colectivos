# -*- coding: utf-8 -*-
import fitz

pdf = fitz.open(r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf')

print('=== TEXTO EXACTO PAGINAS CLAVE SIL ===')

# Página 17 - Becas
print('\n--- PAGINA 17 (BECAS) ---')
print(pdf[16].get_text()[:1500])

# Página 20 - Uniformes
print('\n--- PAGINA 20 (UNIFORMES) ---')
print(pdf[19].get_text()[:1500])

# Página 25 - Casino
print('\n--- PAGINA 25 (CASINO) ---')
print(pdf[24].get_text()[:1500])

pdf.close()
