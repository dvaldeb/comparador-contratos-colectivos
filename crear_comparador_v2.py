# -*- coding: utf-8 -*-
import fitz
import os
import re
import webbrowser

print('=== CREANDO COMPARADOR MEJORADO ===')
print()

output_html = r'c:\Users\dvaldeb\pupy inteeligente\comparador_clausulas_v2.html'

# Temas con keywords expandidos para Casino/Alimentación
temas = {
    'Excelencia Académica': {
        'keywords': ['excelencia acad', 'beca', 'becas', 'escolaridad', 'premio mejor'],
        'icono': '🎓',
        'color': '#2A8703'
    },
    'Aniversarios': {
        'keywords': ['aniversario', 'años de servicio', 'celebrarán su aniversario'],
        'icono': '🎉',
        'color': '#0053E2'
    },
    'Casino / Alimentación': {
        'keywords': ['casino', 'alimentación', 'colación', 'bono de alimentación', 'almuerzo', 
                     'menú', 'mejorado', 'comida', 'comedor', 'ración'],
        'icono': '🍽️',
        'color': '#E91E63',
        'extraer_completo': True  # Flag para extraer todo
    },
    'Uniformes': {
        'keywords': ['uniforme', 'ropa de trabajo', 'vestuario', 'vestimenta'],
        'icono': '👔',
        'color': '#76C8E8'
    }
}

pdfs_config = [
    {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf',
        'nombre': 'SIL',
        'nombre_completo': 'Sindicato Interempresa Líder',
        'version': 'CC SIL 2025-2027 (Firma 02.07.2025)',
        'marcas': ['Hiper', 'Express', 'Ekono', 'Walmart Mayorista'],
        'color': '#0053E2'
    },
    {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf',
        'nombre': 'FED WM',
        'nombre_completo': 'Federación Nacional Walmart',
        'version': 'CC FED WM 15.12.2025 (Versión Definitiva)',
        'marcas': ['Hiper', 'Express', 'Ekono', 'Acuenta', 'SBA'],
        'color': '#FFC220'
    }
]

def extraer_clausula_simple(pdf, keywords):
    """Extrae cláusula estándar"""
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_lower = texto.lower()
        
        for kw in keywords:
            if kw.lower() in texto_lower:
                idx = texto_lower.find(kw.lower())
                inicio = max(0, idx - 150)
                
                for i in range(idx, max(0, idx-150), -1):
                    if re.search(r'\d+[.\-\)]\s*[A-Z]', texto[max(0,i-5):i+5]):
                        inicio = max(0, i-5)
                        break
                
                fin = min(len(texto), idx + 1800)
                for i in range(idx + 100, min(len(texto), idx + 1800)):
                    if re.search(r'^\s*\d+[.\-\)]\s*[A-Z]', texto[i:i+15]):
                        fin = i
                        break
                
                clausula = texto[inicio:fin].strip()
                clausula = re.sub(r'\n\s*\n+', '\n', clausula)
                
                if len(clausula) > 50:
                    return {'pagina': page_num + 1, 'texto': clausula}
    return None

def extraer_casino_completo(pdf):
    """Extrae TODO lo relacionado con Casino/Alimentación"""
    keywords_casino = [
        'casino', 'alimentación', 'colación', 'almuerzo', 'comida', 'comedor',
        'menú', 'mejorado', 'mejorados', 'ración', 'dieta', 'turno',
        'horario de alimentación', 'bono de alimentación', 'ticket', 'vale'
    ]
    
    secciones = []
    paginas_encontradas = set()
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_lower = texto.lower()
        
        # Verificar si la página tiene contenido de casino
        tiene_casino = False
        for kw in keywords_casino:
            if kw in texto_lower:
                tiene_casino = True
                break
        
        if tiene_casino and page_num not in paginas_encontradas:
            paginas_encontradas.add(page_num)
            
            # Extraer secciones relevantes
            # Buscar artículos/numerales
            patron = r'(\d+[.\-\)]\s*(?:CASINO|ALIMENTACI|COLACI|MENÚ|MEJORADO|COMIDA|ALMUERZO)[^\d]*?)(?=\d+[.\-\)]\s*[A-Z]|$)'
            matches = re.findall(patron, texto, re.IGNORECASE | re.DOTALL)
            
            if matches:
                for match in matches:
                    if len(match) > 50:
                        secciones.append({
                            'pagina': page_num + 1,
                            'texto': match.strip()
                        })
            else:
                # Si no encuentra patron, extraer toda la sección de casino
                for kw in ['casino', 'alimentación', 'colación']:
                    if kw in texto_lower:
                        idx = texto_lower.find(kw)
                        inicio = max(0, idx - 100)
                        
                        # Buscar inicio de artículo
                        for i in range(idx, max(0, idx-100), -1):
                            if re.search(r'\d+[.\-\)]', texto[max(0,i-3):i+3]):
                                inicio = max(0, i-3)
                                break
                        
                        # Buscar fin (siguiente artículo o fin de página)
                        fin = len(texto)
                        for i in range(idx + 200, len(texto)):
                            if re.search(r'^\s*\d+[.\-\)]\s*[A-Z]', texto[i:i+15]):
                                # Verificar que no sea parte de casino
                                next_section = texto[i:i+50].lower()
                                if not any(ck in next_section for ck in ['casino', 'alimenta', 'menú', 'mejorad', 'colaci']):
                                    fin = i
                                    break
                        
                        seccion = texto[inicio:fin].strip()
                        if len(seccion) > 100 and seccion not in [s['texto'] for s in secciones]:
                            secciones.append({
                                'pagina': page_num + 1,
                                'texto': seccion
                            })
                        break
    
    # Consolidar secciones
    if secciones:
        texto_completo = ""
        paginas = []
        for s in secciones:
            if s['pagina'] not in paginas:
                paginas.append(s['pagina'])
            texto_completo += f"\n\n--- PÁGINA {s['pagina']} ---\n\n{s['texto']}"
        
        return {
            'pagina': ', '.join(map(str, sorted(paginas))),
            'texto': texto_completo.strip()
        }
    
    return None

# Extraer datos
datos = {}
for config in pdfs_config:
    print(f'Procesando: {config["nombre"]}')
    pdf = fitz.open(config['path'])
    datos[config['nombre']] = {'config': config, 'temas': {}}
    
    for tema, tema_config in temas.items():
        if tema == 'Casino / Alimentación':
            # Extracción especial para casino
            resultado = extraer_casino_completo(pdf)
            if resultado:
                print(f'  {tema}: Págs {resultado["pagina"]} (extracción completa)')
                datos[config['nombre']]['temas'][tema] = resultado
            else:
                datos[config['nombre']]['temas'][tema] = {'pagina': '-', 'texto': 'No encontrado'}
        else:
            resultado = extraer_clausula_simple(pdf, tema_config['keywords'])
            if resultado:
                print(f'  {tema}: Pág {resultado["pagina"]}')
                datos[config['nombre']]['temas'][tema] = resultado
            else:
                datos[config['nombre']]['temas'][tema] = {'pagina': '-', 'texto': 'No encontrado'}
    
    pdf.close()

print()
print('Generando HTML mejorado...')

# Generar HTML
html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comparador de Cláusulas - Contratos Colectivos</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .walmart-blue { background-color: #0053E2; }
        .walmart-spark { background-color: #FFC220; }
        .tab-active { border-bottom: 4px solid #0053E2; background-color: #E6F0FF; font-weight: bold; }
        .sind-btn-active { transform: scale(1.05); box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .clausula-box { 
            white-space: pre-wrap; 
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.7;
            font-size: 14px;
        }
        .section-divider {
            background: linear-gradient(90deg, #0053E2, #FFC220);
            height: 3px;
            margin: 20px 0;
        }
        @media print {
            .no-print { display: none; }
        }
    </style>
</head>
<body class="bg-gray-100">
    <!-- Header -->
    <header class="walmart-blue text-white py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">📊 Comparador de Cláusulas</h1>
            <p class="text-blue-100 mt-2">Contratos Colectivos - Selección por Sindicato</p>
        </div>
    </header>

    <div class="container mx-auto px-4 py-6">
        
        <!-- Tabs de Temas -->
        <div class="bg-white rounded-t-xl shadow-lg">
            <div class="flex border-b no-print" id="tabs">
'''

# Tabs de temas
for i, (tema, config) in enumerate(temas.items()):
    active = 'tab-active' if i == 0 else ''
    tema_id = tema.replace(' ', '_').replace('/', '_')
    html += f'''                <button onclick="showTab('{tema_id}')" 
                        class="flex-1 py-4 px-2 text-center hover:bg-gray-100 transition-all {active}" 
                        id="tab-{tema_id}">
                    <span class="text-2xl">{config['icono']}</span><br>
                    <span class="text-sm">{tema}</span>
                </button>
'''

html += '''            </div>
        </div>

        <!-- Contenido -->
        <div class="bg-white rounded-b-xl shadow-lg p-6">
'''

# Contenido de cada tab
for i, (tema, tema_config) in enumerate(temas.items()):
    display = 'block' if i == 0 else 'none'
    tema_id = tema.replace(' ', '_').replace('/', '_')
    
    html += f'''            <div id="content-{tema_id}" style="display: {display}">
                <h2 class="text-2xl font-bold mb-4" style="color: {tema_config['color']}">
                    {tema_config['icono']} {tema}
                </h2>
                
                <!-- Botones de Sindicato -->
                <div class="flex flex-wrap gap-4 mb-6 no-print">
'''
    
    # Botones por sindicato
    for j, (sind_nombre, sind_data) in enumerate(datos.items()):
        config = sind_data['config']
        active_class = 'sind-btn-active' if j == 0 else 'opacity-70'
        html += f'''                    <button onclick="showSindicato('{tema_id}', '{sind_nombre}')" 
                            id="btn-{tema_id}-{sind_nombre}"
                            class="flex-1 min-w-[200px] p-4 rounded-xl text-white font-bold transition-all hover:opacity-100 {active_class}"
                            style="background-color: {config['color']}">
                        <div class="text-lg">{config['nombre']}</div>
                        <div class="text-xs opacity-80">{config['nombre_completo']}</div>
                        <div class="text-xs mt-2 opacity-60">{', '.join(config['marcas'][:3])}...</div>
                    </button>
'''
    
    html += '''                    <button onclick="showSindicato(\'{}\')"
                            id="btn-{}-TODOS"
                            class="min-w-[150px] p-4 rounded-xl bg-gray-800 text-white font-bold transition-all hover:bg-gray-700 opacity-70"
                            >
                        <div class="text-lg">🔍 COMPARAR</div>
                        <div class="text-xs">Ver ambos</div>
                    </button>
                </div>
'''.format(tema_id, tema_id)
    
    # Contenido por sindicato
    for j, (sind_nombre, sind_data) in enumerate(datos.items()):
        config = sind_data['config']
        tema_data = sind_data['temas'].get(tema, {'pagina': '-', 'texto': 'No encontrado'})
        display_sind = 'block' if j == 0 else 'none'
        
        html += f'''                <div id="sind-{tema_id}-{sind_nombre}" class="sindicato-content-{tema_id}" style="display: {display_sind}">
                    <div class="rounded-xl overflow-hidden border-2" style="border-color: {config['color']}">
                        <div class="px-6 py-4 text-white" style="background-color: {config['color']}">
                            <div class="flex justify-between items-center">
                                <div>
                                    <h3 class="text-xl font-bold">{config['nombre']}</h3>
                                    <p class="text-sm opacity-80">{config['nombre_completo']}</p>
                                </div>
                                <div class="text-right">
                                    <div class="bg-white/20 px-3 py-1 rounded-full text-sm">Pág {tema_data['pagina']}</div>
                                    <div class="text-xs mt-1 opacity-70">{config['version']}</div>
                                </div>
                            </div>
                            <div class="flex flex-wrap gap-2 mt-3">
'''
        for marca in config['marcas']:
            html += f'                                <span class="bg-white/20 px-2 py-1 rounded text-xs">{marca}</span>\n'
        
        html += f'''                            </div>
                        </div>
                        <div class="p-6 bg-gray-50">
                            <div class="clausula-box bg-white p-6 rounded-lg border max-h-[600px] overflow-y-auto">
{tema_data['texto']}
                            </div>
                        </div>
                    </div>
                </div>
'''
    
    # Vista comparativa (TODOS)
    html += f'''                <div id="sind-{tema_id}-TODOS" class="sindicato-content-{tema_id}" style="display: none">
                    <div class="grid md:grid-cols-2 gap-6">
'''
    
    for sind_nombre, sind_data in datos.items():
        config = sind_data['config']
        tema_data = sind_data['temas'].get(tema, {'pagina': '-', 'texto': 'No encontrado'})
        
        html += f'''                        <div class="rounded-xl overflow-hidden border-2" style="border-color: {config['color']}">
                            <div class="px-4 py-3 text-white font-bold" style="background-color: {config['color']}">
                                <span>{config['nombre']}</span>
                                <span class="float-right bg-white/20 px-2 py-1 rounded text-sm">Pág {tema_data['pagina']}</span>
                            </div>
                            <div class="p-4 bg-gray-50">
                                <div class="clausula-box bg-white p-4 rounded border max-h-[500px] overflow-y-auto text-sm">
{tema_data['texto']}
                                </div>
                            </div>
                        </div>
'''
    
    html += '''                    </div>
                </div>
            </div>
'''

html += '''        </div>

        <!-- Botón Imprimir -->
        <div class="mt-6 text-center no-print">
            <button onclick="window.print()" class="walmart-blue text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition mr-4">
                🖨️ Imprimir
            </button>
            <button onclick="exportarTexto()" class="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition">
                💾 Exportar Texto
            </button>
        </div>
    </div>

    <footer class="bg-gray-800 text-white py-4 mt-8">
        <div class="container mx-auto px-4 text-center text-sm">
            <p>Generado por Code Puppy 🐶 | Walmart Chile</p>
        </div>
    </footer>

    <script>
        function showTab(tema) {
            document.querySelectorAll('[id^="content-"]').forEach(el => el.style.display = 'none');
            document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.remove('tab-active'));
            document.getElementById('content-' + tema).style.display = 'block';
            document.getElementById('tab-' + tema).classList.add('tab-active');
        }
        
        function showSindicato(tema, sindicato) {
            // Ocultar todos los contenidos de sindicato para este tema
            document.querySelectorAll('.sindicato-content-' + tema).forEach(el => el.style.display = 'none');
            
            // Desactivar todos los botones
            document.querySelectorAll('[id^="btn-' + tema + '-"]').forEach(el => {
                el.classList.remove('sind-btn-active');
                el.classList.add('opacity-70');
            });
            
            // Mostrar el sindicato seleccionado
            const targetId = sindicato ? 'sind-' + tema + '-' + sindicato : 'sind-' + tema + '-TODOS';
            document.getElementById(targetId).style.display = 'block';
            
            // Activar botón
            const btnId = sindicato ? 'btn-' + tema + '-' + sindicato : 'btn-' + tema + '-TODOS';
            const btn = document.getElementById(btnId);
            btn.classList.add('sind-btn-active');
            btn.classList.remove('opacity-70');
        }
        
        function exportarTexto() {
            const content = document.body.innerText;
            const blob = new Blob([content], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'comparativo_clausulas.txt';
            a.click();
        }
    </script>
</body>
</html>
'''

# Guardar
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'HTML guardado: {output_html}')
webbrowser.open(output_html)
print('Abriendo en navegador...')
