# -*- coding: utf-8 -*-
import fitz
import os
import re
import webbrowser

print('=== CREANDO COMPARADOR VISUAL DE CLAUSULAS ===')
print()

# Configuración
output_html = r'c:\Users\dvaldeb\pupy inteeligente\comparador_clausulas.html'

temas = {
    'Excelencia Académica': {
        'keywords': ['excelencia acad', 'beca', 'becas', 'escolaridad', 'premio mejor'],
        'icono': '🎓',
        'color': '#2A8703'  # Verde
    },
    'Aniversarios': {
        'keywords': ['aniversario', 'años de servicio', 'celebrarán su aniversario'],
        'icono': '🎉',
        'color': '#0053E2'  # Azul Walmart
    },
    'Casino / Alimentación': {
        'keywords': ['casino', 'alimentación', 'colación', 'bono de alimentación'],
        'icono': '🍽️',
        'color': '#FFC220'  # Spark
    },
    'Uniformes': {
        'keywords': ['uniforme', 'ropa de trabajo', 'vestuario', 'vestimenta'],
        'icono': '👔',
        'color': '#76C8E8'  # Cyan
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

def extraer_clausula(pdf, keywords):
    """Extrae cláusula completa"""
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

# Extraer datos de los PDFs
datos = {}
for config in pdfs_config:
    print(f'Procesando: {config["nombre"]}')
    pdf = fitz.open(config['path'])
    datos[config['nombre']] = {'config': config, 'temas': {}}
    
    for tema, tema_config in temas.items():
        resultado = extraer_clausula(pdf, tema_config['keywords'])
        if resultado:
            datos[config['nombre']]['temas'][tema] = resultado
            print(f'  {tema}: Pág {resultado["pagina"]}')
        else:
            datos[config['nombre']]['temas'][tema] = {'pagina': '-', 'texto': 'No encontrado'}
    
    pdf.close()

print()
print('Generando HTML...')

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
        .tab-active { border-bottom: 3px solid #0053E2; background-color: #E6F0FF; }
        .clausula-box { 
            white-space: pre-wrap; 
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.6;
        }
        .highlight { background-color: #FFF3CD; padding: 2px 4px; border-radius: 3px; }
        @media print {
            .no-print { display: none; }
            .print-break { page-break-before: always; }
        }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="walmart-blue text-white py-6 shadow-lg">
        <div class="container mx-auto px-4">
            <h1 class="text-3xl font-bold">📊 Comparador de Cláusulas</h1>
            <p class="text-blue-100 mt-2">Contratos Colectivos - Análisis Comparativo</p>
        </div>
    </header>

    <!-- Info Cards -->
    <div class="container mx-auto px-4 py-6">
        <div class="grid md:grid-cols-2 gap-4 mb-6">
'''

# Cards de sindicatos
for config in pdfs_config:
    marcas_html = ' '.join([f'<span class="bg-white/20 px-2 py-1 rounded text-sm">{m}</span>' for m in config['marcas']])
    html += f'''
            <div class="rounded-lg p-4 text-white shadow-lg" style="background-color: {config['color']}">
                <h3 class="text-xl font-bold">{config['nombre']}</h3>
                <p class="text-sm opacity-90">{config['nombre_completo']}</p>
                <p class="text-xs mt-2 opacity-75">{config['version']}</p>
                <div class="mt-3 flex flex-wrap gap-2">{marcas_html}</div>
            </div>
'''

html += '''        </div>

        <!-- Tabs de Temas -->
        <div class="bg-white rounded-lg shadow-lg overflow-hidden">
            <div class="flex border-b no-print" id="tabs">
'''

# Tabs
for i, (tema, config) in enumerate(temas.items()):
    active = 'tab-active' if i == 0 else ''
    html += f'''                <button onclick="showTab('{tema.replace(' ', '_').replace('/', '_')}')" 
                        class="flex-1 py-4 px-4 text-center font-semibold hover:bg-gray-100 transition {active}" 
                        id="tab-{tema.replace(' ', '_').replace('/', '_')}">
                    <span class="text-2xl">{config['icono']}</span><br>
                    <span class="text-sm">{tema}</span>
                </button>
'''

html += '''            </div>

            <!-- Contenido de Tabs -->
'''

# Contenido de cada tab
for i, (tema, tema_config) in enumerate(temas.items()):
    display = 'block' if i == 0 else 'none'
    tema_id = tema.replace(' ', '_').replace('/', '_')
    
    html += f'''            <div id="content-{tema_id}" class="p-6" style="display: {display}">
                <h2 class="text-2xl font-bold mb-4" style="color: {tema_config['color']}">
                    {tema_config['icono']} {tema}
                </h2>
                
                <div class="grid md:grid-cols-2 gap-6">
'''
    
    for sind_nombre, sind_data in datos.items():
        tema_data = sind_data['temas'].get(tema, {'pagina': '-', 'texto': 'No encontrado'})
        config = sind_data['config']
        
        html += f'''                    <div class="border-2 rounded-lg overflow-hidden" style="border-color: {config['color']}">
                        <div class="px-4 py-3 text-white font-bold flex justify-between items-center" style="background-color: {config['color']}">
                            <span>{config['nombre']}</span>
                            <span class="bg-white/20 px-2 py-1 rounded text-sm">Pág {tema_data['pagina']}</span>
                        </div>
                        <div class="p-4 bg-gray-50">
                            <div class="text-xs text-gray-500 mb-2">Marcas: {', '.join(config['marcas'])}</div>
                            <div class="clausula-box text-sm text-gray-700 max-h-96 overflow-y-auto bg-white p-4 rounded border">
{tema_data['texto']}
                            </div>
                        </div>
                    </div>
'''
    
    html += '''                </div>
            </div>
'''

html += '''        </div>

        <!-- Botón Imprimir -->
        <div class="mt-6 text-center no-print">
            <button onclick="window.print()" class="walmart-blue text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition">
                🖨️ Imprimir / Exportar PDF
            </button>
        </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-4 mt-8">
        <div class="container mx-auto px-4 text-center text-sm">
            <p>Generado por Code Puppy 🐶 | Walmart Chile</p>
        </div>
    </footer>

    <script>
        function showTab(tema) {
            // Ocultar todos los contenidos
            document.querySelectorAll('[id^="content-"]').forEach(el => el.style.display = 'none');
            // Desactivar todos los tabs
            document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.remove('tab-active'));
            // Mostrar contenido seleccionado
            document.getElementById('content-' + tema).style.display = 'block';
            // Activar tab seleccionado
            document.getElementById('tab-' + tema).classList.add('tab-active');
        }
    </script>
</body>
</html>
'''

# Guardar HTML
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'HTML guardado: {output_html}')

# Abrir en navegador
webbrowser.open(output_html)
print('Abriendo en navegador...')
