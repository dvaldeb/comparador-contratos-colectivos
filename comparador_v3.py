# -*- coding: utf-8 -*-
import fitz
import re
import webbrowser

print('='*70)
print('COMPARADOR V3 - CLAUSULAS POR FORMATO (CORREGIDO)')
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

# Temas - Excelencia Académica SOLO becas, sin cumpleaños
TEMAS = {
    'Excelencia Académica': {'icono': '🎓', 'color': '#2A8703'},
    'Aniversarios': {'icono': '🎉', 'color': '#0053E2'},
    'Casino / Alimentación': {'icono': '🍽️', 'color': '#E91E63'},
    'Uniformes': {'icono': '👔', 'color': '#76C8E8'}
}

# Configuración de PDFs con mapeo de páginas por formato y tema
# Basado en análisis detallado de cada documento
pdfs_config = {
    'SIL': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\SIL_2025.pdf',
        'nombre_completo': 'Sindicato Interempresa Líder',
        'version': 'CC SIL 2025-2027',
        'color': '#0053E2',
        'marcas': {
            # Título III: Hiper y Express (pág 9-28)
            'Hiper': {'Excelencia Académica': 17, 'Aniversarios': 26, 'Casino / Alimentación': 25, 'Uniformes': 20},
            'Express': {'Excelencia Académica': 17, 'Aniversarios': 26, 'Casino / Alimentación': 25, 'Uniformes': 20},
            # Título IV: Abarrotes Económicos = SBA/Acuenta (pág 29-43)
            'Acuenta / SBA': {'Excelencia Académica': 37, 'Aniversarios': None, 'Casino / Alimentación': 43, 'Uniformes': 39},
            # Ekono = Express 400 (pág 44-52)
            'Express 400': {'Excelencia Académica': 49, 'Aniversarios': None, 'Casino / Alimentación': 43, 'Uniformes': 51},
            # Título VI: Walmart Mayorista (pág 53-60)
            'Walmart Mayorista': {'Excelencia Académica': 55, 'Aniversarios': None, 'Casino / Alimentación': None, 'Uniformes': 57}
        }
    },
    'FED WM': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FED_WM_2025.pdf',
        'nombre_completo': 'Federación Nacional Walmart',
        'version': 'CC FED WM 2025',
        'color': '#FFC220',
        'marcas': {
            # Capítulo I: Cláusulas para TODOS (pág 6+)
            # Becas pág 10, Aniversario pág 11, Casino pág 24
            'Hiper': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 19},
            'Express': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 19},
            # Cap III: Abarrotes Económicos = SBA/Acuenta (pág 34+)
            'Acuenta / SBA': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 48},
            # Cap V: Ekono = Express 400 (pág 50+)
            'Express 400': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 53},
            # Cap IV: Mayorista (pág 45+)
            'Walmart Mayorista': {'Excelencia Académica': 10, 'Aniversarios': 11, 'Casino / Alimentación': 24, 'Uniformes': 44}
        }
    },
    'FENATRALID': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FENATRALID_2024.pdf',
        'nombre_completo': 'Fed. Nac. Trab. Líder',
        'version': 'CC FENATRALID 2024-2026',
        'color': '#E91E63',
        'marcas': {
            # Cap 2: Cláusulas para Hiper/Express (pág 19+)
            # Becas pág 43, Aniversario pág 40, Casino pág 34, Uniformes pág 32
            'Hiper': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            'Express': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            # Cap 3 II: Abarrotes Económicos = SBA/Acuenta (pág 54+)
            'Acuenta / SBA': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            # Cap 3 IV: Ekono = Express 400 (pág 62+)
            'Express 400': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32},
            # Cap 3 III: Mayorista (pág 59+)
            'Walmart Mayorista': {'Excelencia Académica': 43, 'Aniversarios': 40, 'Casino / Alimentación': 34, 'Uniformes': 32}
        }
    },
    'FSA': {
        'path': r'c:\Users\dvaldeb\pupy inteeligente\contratos\FSA_2024.pdf',
        'nombre_completo': 'Federación Sind. Autónoma',
        'version': 'CC FSA 2024-2026',
        'color': '#9C27B0',
        'marcas': {
            # Solo Hiper y Express
            'Hiper': {'Excelencia Académica': 26, 'Aniversarios': 21, 'Casino / Alimentación': 14, 'Uniformes': 11},
            'Express': {'Excelencia Académica': 26, 'Aniversarios': 21, 'Casino / Alimentación': 14, 'Uniformes': 11},
            'Express 400': None,
            'Acuenta / SBA': None,
            'Walmart Mayorista': None
        }
    }
}

def normalizar(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def extraer_clausula_becas(pdf, pagina):
    """Extrae SOLO la cláusula de BECAS COMPLETA, excluyendo cumpleaños"""
    if pagina is None:
        return None
    
    page_idx = pagina - 1
    if page_idx < 0 or page_idx >= len(pdf):
        return None
    
    # Obtener texto de la página y la siguiente
    page = pdf[page_idx]
    texto = page.get_text()
    
    # Agregar siguiente página para tener texto completo
    if page_idx + 1 < len(pdf):
        texto += "\n" + pdf[page_idx + 1].get_text()
    if page_idx + 2 < len(pdf):
        texto += "\n" + pdf[page_idx + 2].get_text()
    
    texto_norm = normalizar(texto.upper())
    
    # Buscar inicio de BECAS
    inicio = 0
    for kw in ['BECAS ESCOLARES', 'BECAS Y PRESTAMOS ESCOLARES', 'BECAS ANUALES']:
        kw_norm = normalizar(kw)
        patron = r'\d+[.\-\):\s]*' + re.escape(kw_norm)
        match = re.search(patron, texto_norm)
        if match:
            inicio = match.start()
            break
    
    if inicio == 0:
        if 'BECAS ESCOLARES' in texto_norm:
            inicio = texto_norm.find('BECAS ESCOLARES')
            # Retroceder para incluir el número
            for i in range(inicio, max(0, inicio-10), -1):
                if texto[i].isdigit():
                    inicio = i
                    break
    
    texto_desde_inicio = texto[inicio:]
    texto_norm_desde = normalizar(texto_desde_inicio.upper())
    
    # Buscar FIN de becas - patrón: número + CUMPLEAÑOS
    fin = len(texto_desde_inicio)
    
    # Buscar "9.- CUMPLEAÑOS" o similar
    patron_fin = r'\d+[.\-\):\s]*(CUMPLEA|NACIMIENTO DE HIJO|BONO POR NACIMIENTO)'
    match_fin = re.search(patron_fin, texto_norm_desde)
    if match_fin:
        fin = match_fin.start()
    
    clausula = texto_desde_inicio[:fin].strip()
    
    # Limpiar saltos de línea excesivos
    clausula = re.sub(r'\n\s*\n\s*\n+', '\n\n', clausula)
    
    # Determinar páginas
    if len(clausula) > 1500:
        pagina_str = f"{pagina}-{pagina+1}"
    else:
        pagina_str = str(pagina)
    
    return {'pagina': pagina_str, 'texto': clausula}

def extraer_clausula_generica(pdf, pagina, keywords, fin_keywords):
    """Extrae una cláusula genérica"""
    if pagina is None:
        return None
    
    page_idx = pagina - 1
    if page_idx < 0 or page_idx >= len(pdf):
        return None
    
    page = pdf[page_idx]
    texto = page.get_text()
    texto_norm = normalizar(texto.upper())
    
    # Buscar inicio
    inicio = 0
    for kw in keywords:
        kw_norm = normalizar(kw)
        patron = r'\d+[.\-\):\s]*' + re.escape(kw_norm)
        match = re.search(patron, texto_norm)
        if match:
            inicio = match.start()
            break
    
    if inicio == 0:
        for kw in keywords:
            kw_norm = normalizar(kw)
            if kw_norm in texto_norm:
                idx = texto_norm.find(kw_norm)
                # Buscar inicio de línea
                for i in range(idx, max(0, idx-50), -1):
                    if texto[i] == '\n':
                        inicio = i + 1
                        break
                break
    
    texto_desde_inicio = texto[inicio:]
    
    # Si es corto, agregar siguiente página
    if len(texto_desde_inicio) < 800 and page_idx + 1 < len(pdf):
        next_page = pdf[page_idx + 1]
        texto_desde_inicio += "\n" + next_page.get_text()
        pagina_str = f"{pagina}-{pagina+1}"
    else:
        pagina_str = str(pagina)
    
    # Buscar fin
    texto_norm_desde = normalizar(texto_desde_inicio.upper())
    fin = min(2500, len(texto_desde_inicio))
    
    for fin_kw in fin_keywords:
        patron = r'\d+[.\-\):\s]*' + re.escape(normalizar(fin_kw))
        match = re.search(patron, texto_norm_desde[100:])
        if match:
            posible_fin = match.start() + 100
            if posible_fin < fin:
                fin = posible_fin
    
    clausula = texto_desde_inicio[:fin].strip()
    clausula = re.sub(r'\n\s*\n\s*\n+', '\n\n', clausula)
    
    if len(clausula) > 2500:
        clausula = clausula[:2500] + "\n[...]"
    
    return {'pagina': pagina_str, 'texto': clausula}

# Extraer datos
print('\nExtrayendo cláusulas por formato...')
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
        
        for tema in TEMAS.keys():
            pagina = temas_pags.get(tema)
            
            if tema == 'Excelencia Académica':
                resultado = extraer_clausula_becas(pdf, pagina)
            elif tema == 'Aniversarios':
                resultado = extraer_clausula_generica(pdf, pagina, 
                    ['ANIVERSARIO', 'CELEBRARAN SU ANIVERSARIO'],
                    ['DESCUENTOS', 'ELECCION', 'MEJOR COLABORADOR', 'ASISTENCIA'])
            elif tema == 'Casino / Alimentación':
                resultado = extraer_clausula_generica(pdf, pagina,
                    ['CASINO Y ALIMENTACION', 'CASINO'],
                    ['ELECCION', 'MEJOR COLABORADOR', 'DESCUENTOS', 'UNIFORME', 'ROPA'])
            elif tema == 'Uniformes':
                resultado = extraer_clausula_generica(pdf, pagina,
                    ['ROPA E IMPLEMENTOS', 'ROPA DE TRABAJO', 'UNIFORME'],
                    ['BONO', 'VACACIONES', 'FERIADO', 'JORNADA', 'CASINO', 'PRESTAMO'])
            
            if resultado:
                print(f'  {marca} - {tema}: Pág {resultado["pagina"]} ({len(resultado["texto"])} chars)')
                datos[sind_nombre]['marcas'][marca][tema] = resultado
            else:
                datos[sind_nombre]['marcas'][marca][tema] = {'pagina': '-', 'texto': 'No aplica a este formato'}
    
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
            font-size: 12px;
        }
        .fade-in { animation: fadeIn 0.3s ease-in; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @media print { .no-print { display: none; } }
    </style>
</head>
<body class="bg-gray-100">
    <header class="walmart-blue text-white py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">Comparador de Cl\u00e1usulas por Formato</h1>
            <p class="text-blue-100 mt-2">Selecciona un formato y tema para comparar las cl\u00e1usulas de cada sindicato</p>
        </div>
    </header>

    <div class="container mx-auto px-4 py-6">
        <div class="bg-white rounded-xl shadow-lg p-6 mb-6 no-print">
            <h2 class="text-lg font-bold text-gray-700 mb-4">Selecciona un Formato:</h2>
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
                    Selecciona un formato arriba para ver las cl\u00e1usulas aplicables
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
        
        num_cols = len(sindicatos_aplicables) if sindicatos_aplicables else 1
        
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
                continue
            
            tema_data = marca_data.get(tema, {'pagina': '-', 'texto': 'No encontrado'})
            
            html += f'''                            <div class="border-2 rounded-xl overflow-hidden" style="border-color: {sind_config['color']}">
                                <div class="px-3 py-2 text-white" style="background-color: {sind_config['color']}">
                                    <div class="flex justify-between items-center">
                                        <span class="font-bold text-sm">{sind_nombre}</span>
                                        <span class="bg-white/20 px-2 py-1 rounded text-xs">P\u00e1g {tema_data['pagina']}</span>
                                    </div>
                                    <div class="text-xs opacity-70">{sind_config['version']}</div>
                                </div>
                                <div class="p-2 bg-gray-50 max-h-[450px] overflow-y-auto">
                                    <div class="clausula-box bg-white p-2 rounded border">
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
