# -*- coding: utf-8 -*-
import fitz
import re
import webbrowser

print('='*70)
print('COMPARADOR CORREGIDO - CLAUSULAS POR MARCA')
print('='*70)

output_html = r'c:\Users\dvaldeb\pupy inteeligente\comparador_por_marcas.html'

# Marcas comerciales
MARCAS = {
    'Hiper': {'icono': '🛒', 'color': '#0053E2'},
    'Express': {'icono': '🏪', 'color': '#2A8703'},
    'Express 400': {'icono': '🌟', 'color': '#FFC220'},
    'Acuenta / SBA': {'icono': '📦', 'color': '#E91E63'},
    'Walmart Mayorista': {'icono': '🚚', 'color': '#FF5722'}
}

# Temas
TEMAS = {
    'Excelencia Académica': {'icono': '🎓', 'color': '#2A8703', 'keywords': ['BECAS ESCOLARES', 'BECAS Y PRESTAMOS']},
    'Aniversarios': {'icono': '🎉', 'color': '#0053E2', 'keywords': ['ANIVERSARIO']},
    'Casino / Alimentación': {'icono': '🍽️', 'color': '#E91E63', 'keywords': ['CASINO', 'ALIMENTACION']},
    'Uniformes': {'icono': '👔', 'color': '#76C8E8', 'keywords': ['ROPA E IMPLEMENTOS', 'ROPA DE TRABAJO', 'UNIFORME']}
}

# Configuración de PDFs con mapeo de páginas por marca y tema
pdfs_config = {
    'SIL': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf',
        'nombre_completo': 'Sindicato Interempresa Líder',
        'version': 'CC SIL 2025-2027',
        'color': '#0053E2',
        'marcas': {
            'Hiper': {'Excelencia Académica': 17, 'Aniversarios': 26, 'Casino / Alimentación': 25, 'Uniformes': 20},
            'Express': {'Excelencia Académica': 17, 'Aniversarios': 26, 'Casino / Alimentación': 25, 'Uniformes': 20},
            'Express 400': {'Excelencia Académica': 49, 'Aniversarios': None, 'Casino / Alimentación': 43, 'Uniformes': 51},
            'Acuenta / SBA': {'Excelencia Académica': 37, 'Aniversarios': None, 'Casino / Alimentación': None, 'Uniformes': 39},
            'Walmart Mayorista': {'Excelencia Académica': 55, 'Aniversarios': None, 'Casino / Alimentación': None, 'Uniformes': 57}
        }
    },
    'FED WM': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf',
        'nombre_completo': 'Federación Nacional Walmart',
        'version': 'CC FED WM 2025',
        'color': '#FFC220',
        'marcas': {
            'Hiper': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 19},
            'Express': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 19},
            'Express 400': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 44},
            'Acuenta / SBA': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 48},
            'Walmart Mayorista': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 53}
        }
    },
    'FENATRALID': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FENATRALID_2024.pdf',
        'nombre_completo': 'Fed. Nac. Trab. Líder',
        'version': 'CC FENATRALID 2024-2026',
        'color': '#E91E63',
        'marcas': {
            'Hiper': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            'Express': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            'Express 400': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            'Acuenta / SBA': None,  # No aplica
            'Walmart Mayorista': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32}
        }
    },
    'FSA': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FSA_2024.pdf',
        'nombre_completo': 'Federación Sind. Autónoma',
        'version': 'CC FSA 2024-2026',
        'color': '#9C27B0',
        'marcas': {
            'Hiper': {'Excelencia Académica': 26, 'Aniversarios': 21, 'Casino / Alimentación': 14, 'Uniformes': 11},
            'Express': {'Excelencia Académica': 26, 'Aniversarios': 21, 'Casino / Alimentación': 14, 'Uniformes': 11},
            'Express 400': None,  # No aplica
            'Acuenta / SBA': None,  # No aplica
            'Walmart Mayorista': None  # No aplica
        }
    }
}

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def extraer_clausula(pdf, pagina, tema_keywords, tema_fin_keywords=None):
    """Extrae la cláusula de una página específica"""
    if pagina is None:
        return None
    
    page_idx = pagina - 1  # Convertir a índice 0-based
    if page_idx < 0 or page_idx >= len(pdf):
        return None
    
    page = pdf[page_idx]
    texto = page.get_text()
    texto_norm = normalizar(texto.upper())
    
    # Buscar el inicio de la cláusula
    inicio = 0
    for kw in tema_keywords:
        kw_norm = normalizar(kw.upper())
        patron = r'\d+[.\-\):\s]*' + re.escape(kw_norm)
        match = re.search(patron, texto_norm)
        if match:
            inicio = match.start()
            break
    
    if inicio == 0:
        # Buscar sin número
        for kw in tema_keywords:
            kw_norm = normalizar(kw.upper())
            if kw_norm in texto_norm:
                inicio = texto_norm.find(kw_norm)
                break
    
    # Extraer desde inicio hasta fin de página o siguiente sección
    texto_desde_inicio = texto[inicio:]
    
    # Si es muy corto, agregar siguiente página
    if len(texto_desde_inicio) < 800 and page_idx + 1 < len(pdf):
        next_page = pdf[page_idx + 1]
        texto_desde_inicio += "\n" + next_page.get_text()
        pagina_str = f"{pagina}-{pagina+1}"
    else:
        pagina_str = str(pagina)
    
    # Limitar a ~2500 caracteres
    if len(texto_desde_inicio) > 2500:
        texto_desde_inicio = texto_desde_inicio[:2500] + "\n[...continua...]"
    
    # Limpiar
    texto_desde_inicio = re.sub(r'\n\s*\n\s*\n+', '\n\n', texto_desde_inicio)
    
    return {'pagina': pagina_str, 'texto': texto_desde_inicio.strip()}

# Extraer datos
print('\nExtrayendo cláusulas por marca...')
datos = {}

for sind_nombre, config in pdfs_config.items():
    print(f'\nProcesando: {sind_nombre}')
    pdf = fitz.open(config['path'])
    datos[sind_nombre] = {'config': config, 'marcas': {}}
    
    for marca, temas_pags in config['marcas'].items():
        if temas_pags is None:
            print(f'  {marca}: No aplica')
            datos[sind_nombre]['marcas'][marca] = None
            continue
        
        datos[sind_nombre]['marcas'][marca] = {}
        
        for tema, tema_config in TEMAS.items():
            pagina = temas_pags.get(tema)
            if pagina:
                resultado = extraer_clausula(pdf, pagina, tema_config['keywords'])
                if resultado:
                    print(f'  {marca} - {tema}: Pág {resultado["pagina"]} ({len(resultado["texto"])} chars)')
                    datos[sind_nombre]['marcas'][marca][tema] = resultado
                else:
                    datos[sind_nombre]['marcas'][marca][tema] = {'pagina': '-', 'texto': 'No encontrado'}
            else:
                datos[sind_nombre]['marcas'][marca][tema] = {'pagina': '-', 'texto': 'No aplica a esta marca'}
    
    pdf.close()

print('\nGenerando HTML...')

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
            line-height: 1.6;
            font-size: 13px;
        }
        .fade-in { animation: fadeIn 0.3s ease-in; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @media print { .no-print { display: none; } }
    </style>
</head>
<body class="bg-gray-100">
    <header class="walmart-blue text-white py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">Comparador de Cláusulas por Marca</h1>
            <p class="text-blue-100 mt-2">Selecciona una marca y tema para comparar las cláusulas de cada sindicato</p>
        </div>
    </header>

    <div class="container mx-auto px-4 py-6">
        <div class="bg-white rounded-xl shadow-lg p-6 mb-6 no-print">
            <h2 class="text-lg font-bold text-gray-700 mb-4">Selecciona una Marca:</h2>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
'''

for marca, config in MARCAS.items():
    marca_id = marca.replace(' ', '_').replace('/', '_')
    html += f'''                <button onclick="selectMarca('{marca_id}')" 
                        id="btn-marca-{marca_id}"
                        class="p-4 rounded-xl text-white font-bold transition-all hover:scale-105"
                        style="background-color: {config['color']}">
                    <div class="text-3xl mb-2">{config['icono']}</div>
                    <div class="text-sm">{marca}</div>
                </button>
'''

html += '''            </div>
        </div>

        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
            <div class="flex border-b no-print">
'''

for i, (tema, config) in enumerate(TEMAS.items()):
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
                    \u261d Selecciona una marca arriba para ver las cláusulas aplicables
                </div>
'''

# Contenido por tema y marca
for tema, tema_config in TEMAS.items():
    tema_id = tema.replace(' ', '_').replace('/', '_')
    display = 'block' if tema == 'Excelencia Académica' else 'none'
    
    html += f'''                <div id="content-{tema_id}" class="tema-content" style="display: {display}">
'''
    
    for marca, marca_config in MARCAS.items():
        marca_id = marca.replace(' ', '_').replace('/', '_')
        
        # Contar sindicatos que aplican a esta marca
        sindicatos_aplicables = []
        for sind_nombre, sind_data in datos.items():
            if sind_data['marcas'].get(marca) is not None:
                sindicatos_aplicables.append(sind_nombre)
        
        num_cols = len(sindicatos_aplicables)
        if num_cols == 0:
            num_cols = 1
        
        html += f'''                    <div id="marca-{marca_id}-{tema_id}" class="marca-content marca-{marca_id} fade-in" style="display: none">
                        <h3 class="text-xl font-bold mb-4" style="color: {tema_config['color']}">
                            {tema_config['icono']} {tema} - <span style="color: {marca_config['color']}">{marca_config['icono']} {marca}</span>
                        </h3>
                        <div class="grid md:grid-cols-{min(num_cols, 4)} gap-4">
'''
        
        for sind_nombre, sind_data in datos.items():
            sind_config = sind_data['config']
            marca_data = sind_data['marcas'].get(marca)
            
            if marca_data is None:
                # Sindicato no aplica a esta marca
                continue
            
            tema_data = marca_data.get(tema, {'pagina': '-', 'texto': 'No encontrado'})
            
            html += f'''                            <div class="border-2 rounded-xl overflow-hidden" style="border-color: {sind_config['color']}">
                                <div class="px-4 py-3 text-white" style="background-color: {sind_config['color']}">
                                    <div class="flex justify-between items-center">
                                        <span class="font-bold">{sind_nombre}</span>
                                        <span class="bg-white/20 px-2 py-1 rounded text-xs">Pág {tema_data['pagina']}</span>
                                    </div>
                                    <div class="text-xs opacity-70">{sind_config['version']}</div>
                                </div>
                                <div class="p-3 bg-gray-50 max-h-[500px] overflow-y-auto">
                                    <div class="clausula-box bg-white p-3 rounded border text-sm">
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
                Imprimir / PDF
            </button>
        </div>
    </div>

    <footer class="bg-gray-800 text-white py-4 mt-8">
        <div class="container mx-auto px-4 text-center text-sm">
            <p>Generado por Code Puppy | Walmart Chile</p>
        </div>
    </footer>

    <script>
        let currentMarca = null;
        let currentTema = 'Excelencia_Acad\u00e9mica';
        
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
