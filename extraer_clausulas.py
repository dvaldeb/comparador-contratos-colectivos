# -*- coding: utf-8 -*-
import fitz
import os
import re
import json

contratos_dir = r'c:\Users\dvaldeb\pupy inteeligente\contratos'

# Temas a buscar
temas = {
    'aniversarios': ['aniversario', 'aniversarios', 'anos de servicio', 'a\u00f1os de servicio', 'antiguedad', 'antig\u00fcedad'],
    'excelencia_academica': ['excelencia acad', 'beca', 'becas', 'estudios', 'escolar', 'educaci', 'academico', 'acad\u00e9mico'],
    'uniformes': ['uniforme', 'uniformes', 'vestimenta', 'vestuario', 'ropa de trabajo'],
    'casino': ['casino', 'casinos', 'alimentaci', 'colaci', 'almuerzo', 'comida', 'comedor']
}

resultados = {}

print('=== EXTRAYENDO CLAUSULAS DE CONTRATOS COLECTIVOS ===')
print()

for archivo in os.listdir(contratos_dir):
    if not archivo.endswith('.pdf'):
        continue
    
    sindicato = archivo.replace('.pdf', '')
    print(f'Procesando: {sindicato}')
    
    filepath = os.path.join(contratos_dir, archivo)
    pdf = fitz.open(filepath)
    
    # Extraer todo el texto
    texto_completo = ''
    for page in pdf:
        texto_completo += page.get_text() + '\n'
    
    pdf.close()
    
    # Normalizar texto
    texto_lower = texto_completo.lower()
    
    resultados[sindicato] = {}
    
    for tema, palabras_clave in temas.items():
        clausulas_encontradas = []
        
        for palabra in palabras_clave:
            # Buscar parrafos que contengan la palabra clave
            # Usar regex para encontrar contexto alrededor de la palabra
            patron = r'([A-ZÁÉÍÓÚ\s]{0,50}?' + re.escape(palabra) + r'[^.]*\.(?:[^.]*\.){0,3})'
            matches = re.findall(patron, texto_lower, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                # Limpiar el texto
                texto_limpio = ' '.join(match.split())
                if len(texto_limpio) > 50 and texto_limpio not in clausulas_encontradas:
                    clausulas_encontradas.append(texto_limpio[:500])
        
        # Buscar articulos especificos
        patron_articulo = r'(art[\u00ed\u00edculo\.\s]*\d+[^.]*' + '|'.join(palabras_clave) + r'[^.]*\.(?:[^.]*\.){0,5})'
        matches_art = re.findall(patron_articulo, texto_lower, re.IGNORECASE | re.DOTALL)
        for match in matches_art:
            texto_limpio = ' '.join(match.split())
            if len(texto_limpio) > 50 and texto_limpio not in clausulas_encontradas:
                clausulas_encontradas.append(texto_limpio[:500])
        
        resultados[sindicato][tema] = clausulas_encontradas[:3]  # Max 3 por tema
        print(f'  {tema}: {len(clausulas_encontradas)} clausulas encontradas')
    
    print()

# Guardar resultados
output_path = os.path.join(contratos_dir, 'clausulas_extraidas.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f'Resultados guardados en: {output_path}')
