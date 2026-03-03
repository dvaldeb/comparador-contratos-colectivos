import pandas as pd

# Leer el archivo fuente
df = pd.read_excel(r'c:\Users\dvaldeb\OneDrive - Walmart Inc\Escritorio\Marcacion Sap\export 03.03v.1.xlsx')

# Buscar la columna de numero de personal
col_pers = [c for c in df.columns if 'pers' in c.lower()][0]
print(f'Columna encontrada: {col_pers}')

# Contar repeticiones
conteo = df[col_pers].value_counts()

# Filtrar solo los que se repiten (mas de 1 vez)
repetidos = conteo[conteo > 1].sort_values(ascending=False)

print(f'Total registros: {len(df)}')
print(f'Numeros de personal que se repiten: {len(repetidos)}')

# Crear DataFrame con los resultados
df_resultado = pd.DataFrame({
    'No_Personal': repetidos.index,
    'Cantidad_Repeticiones': repetidos.values
})

# Ordenar por cantidad de repeticiones (mayor a menor)
df_resultado = df_resultado.sort_values('Cantidad_Repeticiones', ascending=False)

# Guardar en Excel
output_path = r'c:\Users\dvaldeb\OneDrive - Walmart Inc\Escritorio\Marcacion Sap\Repetidos_03.03v.1.xlsx'
df_resultado.to_excel(output_path, index=False, sheet_name='Repetidos')

print(f'\nArchivo creado: {output_path}')
print(f'\nPrimeras 20 filas del resultado:')
print(df_resultado.head(20).to_string(index=False))
