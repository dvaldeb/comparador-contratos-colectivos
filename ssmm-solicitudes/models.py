"""Database models for SSMM solicitudes."""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "ssmm.db"


def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabla de solicitudes de servicios mínimos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tienda TEXT NOT NULL,
            mercado TEXT,
            cargo_ssmm TEXT NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            fecha_evento DATE NOT NULL,
            turno TEXT NOT NULL,
            motivo TEXT,
            solicitante_nombre TEXT NOT NULL,
            solicitante_email TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP,
            notas TEXT
        )
    """)
    
    # Tabla de tiendas (para autocompletado)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tiendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            mercado TEXT,
            gt_email TEXT,
            lpt_email TEXT
        )
    """)
    
    # Tabla de cargos SSMM válidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cargos_ssmm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def crear_solicitud(
    tienda: str,
    mercado: str,
    cargo_ssmm: str,
    cantidad: int,
    fecha_evento: str,
    turno: str,
    motivo: str,
    solicitante_nombre: str,
    solicitante_email: str
) -> int:
    """Create a new SSMM request."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO solicitudes 
        (tienda, mercado, cargo_ssmm, cantidad, fecha_evento, turno, motivo, 
         solicitante_nombre, solicitante_email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tienda, mercado, cargo_ssmm, cantidad, fecha_evento, turno, motivo,
          solicitante_nombre, solicitante_email))
    solicitud_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return solicitud_id


def obtener_solicitudes(estado: str = None) -> list:
    """Get all requests, optionally filtered by status."""
    conn = get_db()
    cursor = conn.cursor()
    
    if estado:
        cursor.execute("""
            SELECT * FROM solicitudes WHERE estado = ? 
            ORDER BY fecha_evento ASC, fecha_solicitud DESC
        """, (estado,))
    else:
        cursor.execute("""
            SELECT * FROM solicitudes 
            ORDER BY fecha_evento ASC, fecha_solicitud DESC
        """)
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def actualizar_estado(solicitud_id: int, nuevo_estado: str, notas: str = None):
    """Update request status."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE solicitudes 
        SET estado = ?, notas = ?, fecha_actualizacion = ?
        WHERE id = ?
    """, (nuevo_estado, notas, datetime.now().isoformat(), solicitud_id))
    conn.commit()
    conn.close()


def obtener_tiendas() -> list:
    """Get all stores."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT codigo, mercado FROM tiendas ORDER BY codigo")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def obtener_cargos_ssmm() -> list:
    """Get all valid SSMM positions."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM cargos_ssmm ORDER BY nombre")
    rows = cursor.fetchall()
    conn.close()
    return [row['nombre'] for row in rows]
