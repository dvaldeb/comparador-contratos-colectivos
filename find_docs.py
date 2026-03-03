import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')

# Find all pptx files related to negociacion
base = r'C:\Users\dvaldeb\Walmart Inc\ECO & LPM Desplegados - General\RRSS - RRLL\RELACIONES SINDICALES\Negociaciones Colectivas'
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.pptx'):
            print(os.path.join(root, f), flush=True)

# Also check OneDrive backup
base2 = r'C:\Users\dvaldeb\OneDrive - Walmart Inc\Respaldo notebook\ECO (1)\Relacionamiento Sindical'
if os.path.exists(base2):
    for root, dirs, files in os.walk(base2):
        for f in files:
            if f.endswith(('.pptx', '.xlsx')):
                print(os.path.join(root, f), flush=True)

# Check Estrategia Laboral
base3 = r'C:\Users\dvaldeb\OneDrive - Walmart Inc\Respaldo notebook\ECO (1)\Estrategia Laboral 2025'
if os.path.exists(base3):
    for root, dirs, files in os.walk(base3):
        for f in files:
            print(os.path.join(root, f), flush=True)
