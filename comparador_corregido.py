# -*- coding: utf-8 -*-
import fitz
import re
import webbrowser

print('=== COMPARADOR CORREGIDO - CLAUSULAS PRECISAS ===')
print()

output_html = r'c:\Users\dvaldeb\pupy inteeligente\comparador_por_marcas.html'

# Marcas (basado en portadas de contratos)
MARCAS = {
    'Hiper': {'icono': '🛒', 'color': '#0053E2', 'sindicatos': ['SIL', 'FED WM', 'FENATRALID', 'FSA']},
    'Express': {'icono': '🏪', 'color': '#2A8703', 'sindicatos': ['SIL', 'FED WM', 'FENATRALID', 'FSA']},
    'Express 400': {'icono': '🌟', 'color': '#FFC220', 'sindicatos': ['SIL', 'FED WM', 'FENATRALID']},
    'Acuenta / SBA': {'icono': '📦', 'color': '#E91E63', 'sindicatos': ['SIL', 'FED WM']},
    'Walmart Mayorista': {'icono': '🚚', 'color': '#FF5722', 'sindicatos': ['SIL', 'FED WM', 'FENATRALID']}
}

# Temas con keywords EXACTOS para evitar mezcla
temas = {
    'Excelencia Académica': {
        'titulo_buscar': ['BECAS ESCOLARES', 'BECAS Y PRESTAMOS ESCOLARES', 'BECAS ANUALES', 'BECAS'],
        'fin_buscar': ['CUMPLEA', 'ANIVERSARIO', 'DEPENDENCIAS', 'ROPA DE TRABAJO', 'ROPA E IMPLEMENTOS', 'MEJOR COLABORADOR', 'PREMIO'],
        'icono': '🎓',
        'color': '#2A8703'
    },
    'Aniversarios': {
        'titulo_buscar': ['CELEBRARAN SU ANIVERSARIO', 'CELEBRARA SU ANIVERSARIO', 'ANIVERSARIO'],
        'fin_buscar': ['DESCUENTOS', 'ELECCION', 'MEJOR COLABORADOR', 'PRESTAMO', 'ACTIVIDADES DE RECREACION'],
        'icono': '🎉',
        'color': '#0053E2',
        'buscar_contexto': True  # Buscar en contexto, no solo título
    },
    'Casino / Alimentación': {
        'titulo_buscar': ['CASINO Y ALIMENTACION', 'CASINO', 'ALIMENTACION'],
        'fin_buscar': ['ELECCION', 'MEJOR COLABORADOR', 'DESCUENTOS', 'LOCOMOCION', 'MOVILIZACION'],
        'icono': '🍽️',
        'color': '#E91E63'
    },
    'Uniformes': {
        'titulo_buscar': ['ROPA E IMPLEMENTOS DE TRABAJO', 'ROPA DE TRABAJO', 'UNIFORME', 'VESTUARIO'],
        'fin_buscar': ['BONO VACACIONES', 'VACACIONES', 'FERIADO', 'JORNADA', 'CASINO'],
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
    },
    'FENATRALID': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FENATRALID_2024.pdf',
        'nombre_completo': 'Fed. Nac. Trab. Líder',
        'version': 'CC FENATRALID 2024-2026',
        'color': '#E91E63'
    },
    'FSA': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FSA_2024.pdf',
        'nombre_completo': 'Federación Sind. Autónoma',
        'version': 'CC FSA 2024-2026',
        'color': '#9C27B0'
    }
}

def normalizar(texto):
    """Normaliza texto quitando acentos"""
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def extraer_aniversarios(pdf):
    """Extracción especial para Aniversarios - busca 'celebrarán su aniversario'"""
    keywords = ['celebrarán su aniversario', 'celebrara su aniversario', 'celebrará su aniversario', 'su aniversario']
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_lower = texto.lower()
        
        for kw in keywords:
            if kw.lower() in texto_lower:
                idx = texto_lower.find(kw.lower())
                
                # Buscar inicio del párrafo ("Una vez al año" o inicio de sección)
                inicio = idx
                for i in range(idx, max(0, idx-300), -1):
                    if 'una vez al a' in texto[i:i+15].lower():
                        inicio = i
                        break
                    # Buscar número de sección
                    if re.match(r'^\d+[.\-]', texto[i:i+5]):
                        inicio = i
                        break
                
                # Buscar fin - más amplio para capturar toda la cláusula
                texto_desde_inicio = texto[inicio:]
                
                # Continuar a la siguiente página si es necesario
                if len(texto_desde_inicio) < 500 and page_num + 1 < len(pdf):
                    next_page = pdf[page_num + 1]
                    texto_desde_inicio += "\n" + next_page.get_text()
                
                texto_norm = normalizar(texto_desde_inicio.upper())
                
                fin = min(2000, len(texto_desde_inicio))
                fin_keywords = ['DESCUENTOS', 'ELECCION', 'MEJOR COLABORADOR', 'PRESTAMO', 'ACTIVIDADES DE RECREACION']
                
                for fkw in fin_keywords:
                    patron = r'\d+[.\-\):\s]*' + re.escape(fkw)
                    match = re.search(patron, texto_norm[100:])
                    if match:
                        posible_fin = match.start() + 100
                        if posible_fin < fin:
                            fin = posible_fin
                
                clausula = texto_desde_inicio[:fin].strip()
                clausula = re.sub(r'\n\s*\n+', '\n', clausula)
                
                if len(clausula) > 50:
                    return {'pagina': str(page_num + 1), 'texto': clausula}
    
    return None

def extraer_clausula_precisa(pdf, titulo_buscar, fin_buscar):
    """Extrae SOLO la cláusula específica, sin mezclar temas"""
    
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        texto = page.get_text()
        texto_norm = normalizar(texto.upper())
        
        # Buscar el título de la cláusula
        for titulo in titulo_buscar:
            titulo_norm = normalizar(titulo)
            # Buscar patrón flexible: número + separadores + título
            patron = r'(\d+[.\-\):\s]*' + re.escape(titulo_norm) + r')'
            match = re.search(patron, texto_norm)
            
            if match:
                inicio = match.start()
                
                # Buscar el FIN de la cláusula (siguiente título)
                texto_desde_inicio = texto[inicio:]
                texto_norm_desde_inicio = texto_norm[inicio:]
                
                fin = len(texto_desde_inicio)
                
                # Buscar dónde termina esta cláusula
                for fin_kw in fin_buscar:
                    fin_kw_norm = normalizar(fin_kw)
                    patron_fin = r'\d+[.\-\):\s]*' + re.escape(fin_kw_norm)
                    match_fin = re.search(patron_fin, texto_norm_desde_inicio[100:])  # Después de 100 chars
                    if match_fin:
                        posible_fin = match_fin.start() + 100
                        if posible_fin < fin:
                            fin = posible_fin
                
                clausula = texto_desde_inicio[:fin].strip()
                
                # Si la cláusula es muy corta, agregar la siguiente página
                if len(clausula) < 500 and page_num + 1 < len(pdf):
                    next_page = pdf[page_num + 1]
                    next_texto = next_page.get_text()
                    next_norm = normalizar(next_texto.upper())
                    
                    # Buscar fin en siguiente página
                    fin_next = len(next_texto)
                    for fin_kw in fin_buscar:
                        fin_kw_norm = normalizar(fin_kw)
                        patron_fin = r'\d+[.\-\)]?\s*' + re.escape(fin_kw_norm)
                        match_fin = re.search(patron_fin, next_norm)
                        if match_fin:
                            if match_fin.start() < fin_next:
                                fin_next = match_fin.start()
                    
                    clausula += "\n" + next_texto[:fin_next].strip()
                    pagina = f"{page_num + 1}-{page_num + 2}"
                else:
                    pagina = str(page_num + 1)
                
                # Limpiar
                clausula = re.sub(r'\n\s*\n\s*\n+', '\n\n', clausula)
                
                return {'pagina': pagina, 'texto': clausula}
    
    return None

def extraer_casino_completo(pdf):
    """Extracción especial para Casino/Alimentación"""
    resultado = extraer_clausula_precisa(
        pdf, 
        ['CASINO Y ALIMENTACIÓN', 'CASINO', 'ALIMENTACIÓN'],
        ['UNIFORME', 'ROPA DE TRABAJO', 'LOCOMOCIÓN', 'MOVILIZACIÓN']
    )
    
    if resultado:
        # Buscar secciones adicionales de menú, mejorados, etc.
        texto_adicional = ""
        paginas_adicionales = []
        
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            texto = page.get_text()
            texto_lower = texto.lower()
            
            # Buscar menciones de mejorado, menú, horarios de alimentación
            if any(kw in texto_lower for kw in ['mejorado', 'menú especial', 'turno nocturno', 'horario de alimentación']):
                if str(page_num + 1) not in resultado['pagina']:
                    # Extraer solo la sección relevante
                    for kw in ['mejorado', 'menú']:
                        if kw in texto_lower:
                            idx = texto_lower.find(kw)
                            inicio = max(0, idx - 100)
                            fin = min(len(texto), idx + 800)
                            seccion = texto[inicio:fin]
                            if seccion not in resultado['texto'] and seccion not in texto_adicional:
                                texto_adicional += f"\n\n--- Sección adicional (Pág {page_num + 1}) ---\n{seccion}"
                                paginas_adicionales.append(str(page_num + 1))
                            break
        
        if texto_adicional:
            resultado['texto'] += texto_adicional
            resultado['pagina'] += ", " + ", ".join(paginas_adicionales)
    
    return resultado

# Extraer datos
print('Extrayendo cláusulas precisas...')
datos = {}

for sind_nombre, config in pdfs_config.items():
    print(f'\nProcesando: {sind_nombre}')
    pdf = fitz.open(config['path'])
    datos[sind_nombre] = {'config': config, 'temas': {}}
    
    for tema, tema_config in temas.items():
        if tema == 'Casino / Alimentación':
            resultado = extraer_casino_completo(pdf)
        elif tema == 'Aniversarios':
            resultado = extraer_aniversarios(pdf)
        else:
            resultado = extraer_clausula_precisa(pdf, tema_config['titulo_buscar'], tema_config['fin_buscar'])
        
        if resultado:
            chars = len(resultado['texto'])
            print(f'  {tema}: Pág {resultado["pagina"]} ({chars} chars)')
            datos[sind_nombre]['temas'][tema] = resultado
        else:
            print(f'  {tema}: No encontrado')
            datos[sind_nombre]['temas'][tema] = {'pagina': '-', 'texto': 'No encontrado'}
    
    pdf.close()

print('\nGenerando HTML...')

# Generar HTML (mismo formato pero con datos corregidos)
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
    <header class="walmart-blue text-white py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">🏪 Comparador de Cláusulas por Marca</h1>
            <p class="text-blue-100 mt-2">Selecciona una marca para ver las cláusulas aplicables</p>
        </div>
    </header>

    <div class="container mx-auto px-4 py-6">
        <div class="bg-white rounded-xl shadow-lg p-6 mb-6 no-print">
            <h2 class="text-lg font-bold text-gray-700 mb-4">🎯 Selecciona una Marca:</h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
'''

for marca, config in MARCAS.items():
    marca_id = marca.replace(' ', '_').replace('(', '').replace(')', '')
    sindicatos_str = ', '.join(config['sindicatos'])
    html += f'''                <button onclick="selectMarca('{marca_id}')" 
                        id="btn-marca-{marca_id}"
                        class="p-4 rounded-xl text-white font-bold transition-all hover:scale-105"
                        style="background-color: {config['color']}">
                    <div class="text-3xl mb-2">{config['icono']}</div>
                    <div class="text-sm">{marca}</div>
                    <div class="text-xs opacity-70 mt-1">{sindicatos_str}</div>
                </button>
'''

html += '''            </div>
        </div>

        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="flex border-b no-print">
'''

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
            <div class="p-6">
                <div id="marca-info" class="mb-4 p-4 bg-blue-50 rounded-lg text-center text-gray-600">
                    👆 Selecciona una marca arriba para ver las cláusulas aplicables
                </div>
'''

for i, (tema, tema_config) in enumerate(temas.items()):
    tema_id = tema.replace(' ', '_').replace('/', '_')
    display = 'block' if i == 0 else 'none'
    
    html += f'''                <div id="content-{tema_id}" class="tema-content" style="display: {display}">
'''
    
    for marca, marca_config in MARCAS.items():
        marca_id = marca.replace(' ', '_').replace('(', '').replace(')', '')
        num_sind = len(marca_config['sindicatos'])
        
        html += f'''                    <div id="marca-{marca_id}-{tema_id}" class="marca-content marca-{marca_id} fade-in" style="display: none">
                        <h3 class="text-xl font-bold mb-4" style="color: {tema_config['color']}">
                            {tema_config['icono']} {tema} - <span style="color: {marca_config['color']}">{marca_config['icono']} {marca}</span>
                        </h3>
                        <div class="grid md:grid-cols-{num_sind} gap-6">
'''
        
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
        <div class="mt-6 text-center no-print">
            <button onclick="window.print()" class="walmart-blue text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition">
                🖨️ Imprimir / PDF
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
            document.querySelectorAll('[id^="btn-marca-"]').forEach(btn => btn.classList.remove('marca-active'));
            document.getElementById('btn-marca-' + marca).classList.add('marca-active');
            document.getElementById('marca-info').style.display = 'none';
            showContent();
        }
        
        function selectTema(tema) {
            currentTema = tema;
            document.querySelectorAll('[id^="tab-"]').forEach(tab => tab.classList.remove('tema-active'));
            document.getElementById('tab-' + tema).classList.add('tema-active');
            document.querySelectorAll('.tema-content').forEach(el => el.style.display = 'none');
            document.getElementById('content-' + tema).style.display = 'block';
            if (currentMarca) showContent();
        }
        
        function showContent() {
            if (!currentMarca) return;
            document.querySelectorAll('#content-' + currentTema + ' .marca-content').forEach(el => el.style.display = 'none');
            const content = document.getElementById('marca-' + currentMarca + '-' + currentTema);
            if (content) content.style.display = 'block';
        }
    </script>
</body>
</html>
'''

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\nHTML guardado: {output_html}')
webbrowser.open(output_html)
