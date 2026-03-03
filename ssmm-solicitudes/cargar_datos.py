"""Load data from CSV files into the database."""
import pandas as pd
from pathlib import Path
import sqlite3
from models import DB_PATH, init_db, get_db

DATA_DIR = Path(__file__).parent / "data"


def cargar_datos_csv():
    """Load store and position data from CSV files."""
    init_db()
    conn = get_db()
    cursor = conn.cursor()
    
    # Cargar datos de colaboradores SSMM 2026
    ssmm_file = DATA_DIR / "SSMM 2026.csv"
    if ssmm_file.exists():
        print("Cargando SSMM 2026...")
        df = pd.read_csv(ssmm_file, sep=';', encoding='latin-1')
        
        # Extraer tiendas únicas con su mercado y emails
        tiendas_cols = ['Tienda', 'Mercado', 'GT', 'LPT']
        if all(col in df.columns for col in tiendas_cols):
            tiendas_df = df[tiendas_cols].drop_duplicates()
            for _, row in tiendas_df.iterrows():
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO tiendas (codigo, mercado, gt_email, lpt_email)
                        VALUES (?, ?, ?, ?)
                    """, (str(row['Tienda']), str(row['Mercado']), 
                          str(row.get('GT', '')), str(row.get('LPT', ''))))
                except Exception as e:
                    print(f"Error insertando tienda: {e}")
        
        # Extraer cargos SSMM únicos
        if 'Cargo SSMM' in df.columns:
            cargos = df['Cargo SSMM'].dropna().unique()
            for cargo in cargos:
                cargo_str = str(cargo).strip()
                if cargo_str and cargo_str != '#N/D' and cargo_str != 'nan':
                    try:
                        cursor.execute("""
                            INSERT OR IGNORE INTO cargos_ssmm (nombre) VALUES (?)
                        """, (cargo_str,))
                    except Exception as e:
                        print(f"Error insertando cargo: {e}")
        
        print(f"  - Tiendas cargadas: {len(tiendas_df)}")
        print(f"  - Cargos SSMM cargados: {len(cargos) if 'Cargo SSMM' in df.columns else 0}")
    
    conn.commit()
    conn.close()
    print("¡Datos cargados exitosamente!")


if __name__ == "__main__":
    cargar_datos_csv()
