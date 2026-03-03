# -*- coding: utf-8 -*-
import fitz
import os
import re
import webbrowser

print('=== COMPARADOR POR MARCAS - CLAUSULAS COMPLETAS ===')
print()

output_html = r'c:\Users\dvaldeb\pupy inteeligente\comparador_por_marcas.html'

# Marcas y qué sindicatos las cubren
MARCAS = {
    'Hiper': {
        'icono': '🏪',
        'color': '#0053E2',
        'sindicatos': ['SIL', 'FED WM']
    },
    'Express': {
        'icono': '🛒',
        'color': '#2A8703',
        'sindicatos': ['SIL', 'FED WM']
    },
    'Ekono': {
        'icono': '💰',
        'color': '#FFC220',
        'sindicatos': ['SIL', 'FED WM']
    },
    'Acuenta': {
        'icono': '📦',
        'color': '#E91E63',
        'sindicatos': ['FED WM']
    },
    'SBA (SuperBodega)': {
        'icono': '🏭',
        'color': '#9C27B0',
        'sindicatos': ['FED WM']
    },
    'Walmart Mayorista': {
        'icono': '🚚',
        'color': '#FF5722',
        'sindicatos': ['SIL']
    }
}

# Temas
temas = {
    'Excelencia Académica': {
        'keywords': ['excelencia acad', 'beca', 'becas escolares', 'premio mejor', 'rendimiento escolar'],
        'icono': '🎓',
        'color': '#2A8703'
    },
    'Aniversarios': {
        'keywords': ['aniversario', 'años de servicio', 'celebrarán su aniversario', 'quinquenio'],
        'icono': '🎉',
        'color': '#0053E2'
    },
    'Casino / Alimentación': {
        'keywords': ['casino', 'alimentación', 'colación', 'almuerzo', 'menú', 'mejorado'],
        'icono': '🍽️',
        'color': '#E91E63'
    },
    'Uniformes': {
        'keywords': ['uniforme', 'ropa de trabajo', 'vestuario', 'vestimenta'],
        'icono': '👔',
        'color': '#76C8E8'
    }
}

pdfs_config = {
    'SIL': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf',
        'nombre_completo': 'Sindicato Interempresa Líder',
        'version': 'CC SIL 2025-2027 (Firma 02.07.2025)',
        'color': '#0053E2'
    },
    'FED WM': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf',
        'nombre_completo': 'Federación Nacional Walmart',
        'version': 'CC FED WM 15.12.2025 (Versión Definitiva)',
        'color': '#FFC220'
    }
}

def extraer_clausula_completa(pdf, keywords, max_chars=5000):
    """Extrae la cláusula COMPLETA buscando el artículo entero"""
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_lower = texto.lower()
        
        for kw in keywords:
            if kw.lower() in texto_lower:
                # Encontrar índice de la keyword
                idx = texto_lower.find(kw.lower())
                
                # Buscar inicio del artículo (número + punto/guión)
                inicio = 0
                for i in range(idx, -1, -1):
                    # Buscar patrón de inicio de artículo
                    if i > 0 and re.match(r'^\s*\d+[.\-\):]', texto[i-1:i+10]):
                        inicio = i - 1
                        break
                    # O buscar título en mayúsculas
                    if i > 0 and re.match(r'^\s*[A-ZÁÉÍÓÚ]{3,}', texto[i:i+20]):
                        inicio = i
                        break
                
                if inicio == 0:
                    inicio = max(0, idx - 200)
                
                # Buscar fin del artículo
                # Continuar a la siguiente página si es necesario
                texto_completo = texto[inicio:]
                pagina_fin = page_num
                
                # Si el texto es corto, agregar páginas siguientes
                while len(texto_completo) < max_chars and pagina_fin + 1 < len(pdf):
                    pagina_fin += 1
                    next_page = pdf[pagina_fin]
                    next_texto = next_page.get_text()
                    
                    # Verificar si la siguiente página continúa el tema
                    if any(k.lower() in next_texto.lower() for k in keywords):
                        texto_completo += "\n" + next_texto
                    else:
                        # Buscar si hay un nuevo artículo (número diferente)
                        if re.match(r'^\s*\d+[.\-\)]', next_texto[:20]):
                            break
                        texto_completo += "\n" + next_texto
                        break
                
                # Buscar el fin del artículo (siguiente número de artículo)
                fin = len(texto_completo)
                # Buscar patrón de nuevo artículo después de cierta distancia
                search_start = min(500, len(texto_completo))
                for i in range(search_start, len(texto_completo)):
                    if re.match(r'^\s*\d+[.\-\)]\s*[A-ZÁÉÍÓÚ]', texto_completo[i:i+20]):
                        # Verificar que no sea parte del mismo tema
                        preview = texto_completo[i:i+100].lower()
                        if not any(k.lower() in preview for k in keywords):
                            fin = i
                            break
                
                clausula = texto_completo[:fin].strip()
                
                # Limpiar
                clausula = re.sub(r'\n\s*\n\s*\n+', '\n\n', clausula)
                clausula = re.sub(r' +', ' ', clausula)
                
                if len(clausula) > 100:
                    paginas = f"{page_num + 1}"
                    if pagina_fin > page_num:
                        paginas = f"{page_num + 1}-{pagina_fin + 1}"
                    
                    return {
                        'pagina': paginas,
                        'texto': clausula
                    }
    
    return None

def extraer_todo_casino(pdf):
    """Extracción especial para Casino - busca TODAS las menciones"""
    keywords = ['casino', 'alimentación', 'colación', 'almuerzo', 'menú', 'mejorado', 
                'comida', 'bono de alimentación', 'ticket', 'turno nocturno']
    
    secciones = []
    paginas_procesadas = set()
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_lower = texto.lower()
        
        # Verificar si tiene contenido relevante
        if any(kw in texto_lower for kw in keywords):
            if page_num not in paginas_procesadas:
                paginas_procesadas.add(page_num)
                
                # Extraer toda la página relevante
                # Buscar el inicio del artículo de casino
                for kw in ['casino', 'alimentación']:
                    if kw in texto_lower:
                        idx = texto_lower.find(kw)
                        
                        # Buscar inicio
                        inicio = 0
                        for i in range(idx, -1, -1):
                            if re.match(r'^\s*\d+[.\-\)]', texto[i:i+10]):
                                inicio = i
                                break
                        
                        seccion = texto[inicio:].strip()
                        if len(seccion) > 100:
                            secciones.append({
                                'pagina': page_num + 1,
                                'texto': seccion
                            })
                        break
    
    if secciones:
        # Combinar todas las secciones
        texto_total = ""
        paginas = []
        
        for s in secciones:
            if s['pagina'] not in paginas:
                paginas.append(s['pagina'])
                texto_total += f"\n{'='*60}\nPÁGINA {s['pagina']}\n{'='*60}\n\n{s['texto']}\n"
        
        return {
            'pagina': ', '.join(map(str, sorted(paginas))),
            'texto': texto_total.strip()
        }
    
    return None

# Extraer datos de los PDFs
print('Extrayendo cláusulas completas...')
datos = {}

for sind_nombre, config in pdfs_config.items():
    print(f'\nProcesando: {sind_nombre}')
    pdf = fitz.open(config['path'])
    datos[sind_nombre] = {'config': config, 'temas': {}}
    
    for tema, tema_config in temas.items():
        if tema == 'Casino / Alimentación':
            resultado = extraer_todo_casino(pdf)
        else:
            resultado = extraer_clausula_completa(pdf, tema_config['keywords'])
        
        if resultado:
            chars = len(resultado['texto'])
            print(f'  {tema}: Pág {resultado["pagina"]} ({chars} caracteres)')
            datos[sind_nombre]['temas'][tema] = resultado
        else:
            print(f'  {tema}: No encontrado')
            datos[sind_nombre]['temas'][tema] = {'pagina': '-', 'texto': 'No encontrado en el documento'}
    
    pdf.close()

print('\n\nGenerando HTML por marcas...')

# Generar HTML
html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparador por Marcas - Contratos Colectivos</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .walmart-blue { background-color: #0053E2; }
        .marca-active { transform: scale(1.05); box-shadow: 0 8px 25px rgba(0,0,0,0.3); border: 3px solid white; }
        .tema-active { background-color: #E6F0FF; border-bottom: 4px solid #0053E2; }
        .clausula-box { 
            white-space: pre-wrap; 
            font-family: 'Segoe UI', Tahoma, sans-serif;
            line-height: 1.8;
            font-size: 14px;
        }
        .fade-in { animation: fadeIn 0.3s ease-in; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @media print { .no-print { display: none; } }
    </style>
</head>
<body class="bg-gray-100">
    <!-- Header -->
    <header class="walmart-blue text-white py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">🏪 Comparador de Cláusulas por Marca</h1>
            <p class="text-blue-100 mt-2">Selecciona una marca para ver las cláusulas aplicables</p>
        </div>
    </header>

    <div class="container mx-auto px-4 py-6">
        
        <!-- Selector de Marcas -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-6 no-print">
            <h2 class="text-lg font-bold text-gray-700 mb-4">🎯 Selecciona una Marca:</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
'''

# Botones de marcas
for marca, config in MARCAS.items():
    marca_id = marca.replace(' ', '_').replace('(', '').replace(')', '')
    sindicatos_str = ', '.join(config['sindicatos'])
    html += f'''                <button onclick="selectMarca('{marca_id}')" 
                        id="btn-marca-{marca_id}"
                        class="p-4 rounded-xl text-white font-bold transition-all hover:scale-105 cursor-pointer"
                        style="background-color: {config['color']}">
                    <div class="text-3xl mb-2">{config['icono']}</div>
                    <div class="text-sm">{marca}</div>
                    <div class="text-xs opacity-70 mt-1">{sindicatos_str}</div>
                </button>
'''

html += '''            </div>
        </div>

        <!-- Tabs de Temas -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="flex border-b no-print">
'''

# Tabs de temas
for i, (tema, config) in enumerate(temas.items()):
    tema_id = tema.replace(' ', '_').replace('/', '_')
    active = 'tema-active' if i == 0 else ''
    html += f'''                <button onclick="selectTema('{tema_id}')" 
                        id="tab-{tema_id}"
                        class="flex-1 py-4 px-2 text-center hover:bg-gray-100 transition-all {active}">
                    <span class="text-2xl">{config['icono']}</span><br>
                    <span class="text-sm font-semibold">{tema}</span>
                </button>
'''

html += '''            </div>

            <!-- Contenido -->
            <div class="p-6">
                <div id="marca-info" class="mb-4 p-4 bg-blue-50 rounded-lg text-center text-gray-600">
                    👆 Selecciona una marca arriba para ver las cláusulas aplicables
                </div>
'''

# Contenido por tema
for i, (tema, tema_config) in enumerate(temas.items()):
    tema_id = tema.replace(' ', '_').replace('/', '_')
    display = 'block' if i == 0 else 'none'
    
    html += f'''                <div id="content-{tema_id}" class="tema-content" style="display: {display}">
'''
    
    # Para cada marca
    for marca, marca_config in MARCAS.items():
        marca_id = marca.replace(' ', '_').replace('(', '').replace(')', '')
        
        html += f'''                    <div id="marca-{marca_id}-{tema_id}" class="marca-content marca-{marca_id} fade-in" style="display: none">
                        <h3 class="text-xl font-bold mb-4" style="color: {tema_config['color']}">
                            {tema_config['icono']} {tema} - <span style="color: {marca_config['color']}">{marca_config['icono']} {marca}</span>
                        </h3>
                        
                        <div class="grid md:grid-cols-{len(marca_config['sindicatos'])} gap-6">
'''
        
        # Mostrar cláusulas de los sindicatos que aplican a esta marca
        for sind in marca_config['sindicatos']:
            sind_config = pdfs_config[sind]
            tema_data = datos[sind]['temas'].get(tema, {'pagina': '-', 'texto': 'No encontrado'})
            
            html += f'''                            <div class="border-2 rounded-xl overflow-hidden" style="border-color: {sind_config['color']}">
                                <div class="px-4 py-3 text-white" style="background-color: {sind_config['color']}">
                                    <div class="flex justify-between items-center">
                                        <div>
                                            <span class="font-bold text-lg">{sind}</span>
                                            <span class="text-sm opacity-80 ml-2">({sind_config['nombre_completo']})</span>
                                        </div>
                                        <span class="bg-white/20 px-3 py-1 rounded-full text-sm">Pág {tema_data['pagina']}</span>
                                    </div>
                                    <div class="text-xs opacity-70 mt-1">{sind_config['version']}</div>
                                </div>
                                <div class="p-4 bg-gray-50 max-h-[600px] overflow-y-auto">
                                    <div class="clausula-box bg-white p-4 rounded-lg border">
{tema_data['texto']}
                                    </div>
                                </div>
                            </div>
'''
        
        html += '''                        </div>
                    </div>
'''
    
    html += '''                </div>
'''

html += '''            </div>
        </div>

        <!-- Botones de acción -->
        <div class="mt-6 text-center no-print">
            <button onclick="window.print()" class="walmart-blue text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition mr-4">
                🖨️ Imprimir
            </button>
        </div>
    </div>

    <footer class="bg-gray-800 text-white py-4 mt-8">
        <div class="container mx-auto px-4 text-center text-sm">
            <p>Generado por Code Puppy 🐶 | Walmart Chile</p>
        </div>
    </footer>

    <script>
        let currentMarca = null;
        let currentTema = 'Excelencia_Académica';
        
        function selectMarca(marca) {
            currentMarca = marca;
            
            // Desactivar todos los botones de marca
            document.querySelectorAll('[id^="btn-marca-"]').forEach(btn => {
                btn.classList.remove('marca-active');
            });
            
            // Activar el botón seleccionado
            document.getElementById('btn-marca-' + marca).classList.add('marca-active');
            
            // Ocultar info inicial
            document.getElementById('marca-info').style.display = 'none';
            
            // Mostrar contenido de la marca para el tema actual
            showContent();
        }
        
        function selectTema(tema) {
            currentTema = tema;
            
            // Desactivar todos los tabs
            document.querySelectorAll('[id^="tab-"]').forEach(tab => {
                tab.classList.remove('tema-active');
            });
            
            // Activar el tab seleccionado
            document.getElementById('tab-' + tema).classList.add('tema-active');
            
            // Ocultar todos los contenidos de tema
            document.querySelectorAll('.tema-content').forEach(el => {
                el.style.display = 'none';
            });
            
            // Mostrar el tema seleccionado
            document.getElementById('content-' + tema).style.display = 'block';
            
            // Mostrar contenido si hay marca seleccionada
            if (currentMarca) {
                showContent();
            }
        }
        
        function showContent() {
            if (!currentMarca) return;
            
            // Ocultar todos los contenidos de marca del tema actual
            document.querySelectorAll('#content-' + currentTema + ' .marca-content').forEach(el => {
                el.style.display = 'none';
            });
            
            // Mostrar el contenido de la marca seleccionada
            const contentId = 'marca-' + currentMarca + '-' + currentTema;
            const content = document.getElementById(contentId);
            if (content) {
                content.style.display = 'block';
            }
        }
    </script>
</body>
</html>
'''

# Guardar
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nHTML guardado: {output_html}')
webbrowser.open(output_html)
print('Abriendo en navegador...')
