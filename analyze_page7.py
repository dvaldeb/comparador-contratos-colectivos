# -*- coding: utf-8 -*-
import fitz
import json

pdf_path = r'c:\Users\dvaldeb\Downloads\Proceso Uniforme Modelo To- Be propuesta final 20251204 (1).pdf'

pdf = fitz.open(pdf_path)
page = pdf[6]  # Pagina 7 (indice 6)

print('=== ANALISIS PAGINA 7 ===')
print(f'Dimensiones: {page.rect.width} x {page.rect.height}')
print()

# Extraer texto con formato
print('=== BLOQUES DE TEXTO ===')
text_dict = page.get_text("dict")

for i, block in enumerate(text_dict.get("blocks", [])):
    if block.get("type") == 0:  # Texto
        bbox = block.get("bbox")
        print(f'\nBloque {i}: pos=({bbox[0]:.0f}, {bbox[1]:.0f}) size=({bbox[2]-bbox[0]:.0f}x{bbox[3]-bbox[1]:.0f})')
        
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if text:
                    size = span.get("size", 0)
                    font = span.get("font", "")
                    color = span.get("color", 0)
                    # Convertir color a RGB
                    r = (color >> 16) & 0xFF
                    g = (color >> 8) & 0xFF
                    b = color & 0xFF
                    print(f'  "{text[:50]}" | size={size:.1f} | color=({r},{g},{b}) | font={font}')

print()
print('=== IMAGENES ===')
images = page.get_images(full=True)
for img in images:
    xref = img[0]
    rects = page.get_image_rects(xref)
    for rect in rects:
        print(f'Imagen xref={xref}: pos=({rect.x0:.0f}, {rect.y0:.0f}) size=({rect.width:.0f}x{rect.height:.0f})')

print()
print('=== DIBUJOS/FORMAS ===')
drawings = page.get_drawings()
print(f'Total dibujos: {len(drawings)}')
for i, d in enumerate(drawings[:20]):  # Primeros 20
    rect = d.get("rect")
    fill = d.get("fill")
    color = d.get("color")
    if rect:
        fill_str = f'fill=({fill[0]:.2f},{fill[1]:.2f},{fill[2]:.2f})' if fill else 'no-fill'
        color_str = f'stroke=({color[0]:.2f},{color[1]:.2f},{color[2]:.2f})' if color else 'no-stroke'
        print(f'  Forma {i}: ({rect.x0:.0f},{rect.y0:.0f}) {rect.width:.0f}x{rect.height:.0f} | {fill_str} | {color_str}')

pdf.close()
