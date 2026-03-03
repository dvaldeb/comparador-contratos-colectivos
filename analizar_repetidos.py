import pandas as pd

df = pd.read_excel(r'c:\Users\dvaldeb\OneDrive - Walmart Inc\Escritorio\Marcacion Sap\export 03.03.XLSX')

# La columna tiene encoding raro, busco la que contiene 'pers'
col_pers = [c for c in df.columns if 'pers' in c.lower()][0]

# Contar repeticiones
conteo = df[col_pers].value_counts()

# Filtrar solo los que se repiten (más de 1 vez)
repetidos = conteo[conteo > 1].sort_values(ascending=False)

print(f'Total de registros: {len(df)}')
print(f'Total de No pers. unicos: {df[col_pers].nunique()}')
print(f'No pers. que se repiten (mas de 1 vez): {len(repetidos)}')
print()
print('=' * 50)
print('TOP 30 No PERS. QUE MAS SE REPITEN:')
print('=' * 50)
print(f"{'No pers.':<15} {'Repeticiones':<12}")
print('-' * 30)
for num_pers, count in repetidos.head(30).items():
    print(f'{num_pers:<15} {count:<12}')

print()
print('=' * 50)
print('RESUMEN POR CANTIDAD DE REPETICIONES:')
print('=' * 50)
max_rep = int(repetidos.max()) if len(repetidos) > 0 else 2
for i in range(2, min(11, max_rep + 1)):
    cantidad = len(conteo[conteo == i])
    if cantidad > 0:
        print(f'Aparecen {i} veces: {cantidad} personas')

# Si hay más de 10 repeticiones
mas_de_10 = conteo[conteo > 10]
if len(mas_de_10) > 0:
    print(f'Aparecen mas de 10 veces: {len(mas_de_10)} personas')
