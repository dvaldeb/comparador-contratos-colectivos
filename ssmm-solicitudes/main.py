"""FastAPI application for SSMM requests."""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import datetime, date

from models import (
    init_db, crear_solicitud, obtener_solicitudes,
    actualizar_estado, obtener_tiendas, obtener_cargos_ssmm
)
from cargar_datos import cargar_datos_csv

app = FastAPI(title="Solicitud de Servicios Mínimos", version="1.0.0")

# Static files and templates
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()
    cargar_datos_csv()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with request form."""
    tiendas = obtener_tiendas()
    cargos = obtener_cargos_ssmm()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tiendas": tiendas,
        "cargos": cargos,
        "today": date.today().isoformat()
    })


@app.post("/solicitar", response_class=HTMLResponse)
async def crear_solicitud_ssmm(
    request: Request,
    tienda: str = Form(...),
    mercado: str = Form(""),
    cargo_ssmm: str = Form(...),
    cantidad: int = Form(1),
    fecha_evento: str = Form(...),
    turno: str = Form(...),
    motivo: str = Form(""),
    solicitante_nombre: str = Form(...),
    solicitante_email: str = Form(...)
):
    """Create a new SSMM request."""
    solicitud_id = crear_solicitud(
        tienda=tienda,
        mercado=mercado,
        cargo_ssmm=cargo_ssmm,
        cantidad=cantidad,
        fecha_evento=fecha_evento,
        turno=turno,
        motivo=motivo,
        solicitante_nombre=solicitante_nombre,
        solicitante_email=solicitante_email
    )
    return templates.TemplateResponse("partials/success.html", {
        "request": request,
        "solicitud_id": solicitud_id,
        "mensaje": f"¡Solicitud #{solicitud_id} creada exitosamente!"
    })


@app.get("/solicitudes", response_class=HTMLResponse)
async def ver_solicitudes(request: Request, estado: str = None):
    """View all reqs."""
    solicitudes = obtener_solicitudes(estado)
    return templates.TemplateResponse("solicitudes.html", {
        "request": request,
        "solicitudes": solicitudes,
        "estado_filtro": estado
    })


@app.get("/solicitudes/tabla", response_class=HTMLResponse)
async def tabla_solicitudes(request: Request, estado: str = None):
    """Get requests table partial for HTMX."""
    solicitudes = obtener_solicitudes(estado if estado != "todos" else None)
    return templates.TemplateResponse("partials/tabla_solicitudes.html", {
        "request": request,
        "solicitudes": solicitudes
    })


@app.post("/solicitudes/{solicitud_id}/estado", response_class=HTMLResponse)
async def cambiar_estado(
    request: Request,
    solicitud_id: int,
    estado: str = Form(...),
    notas: str = Form("")
):
    """Update request status."""
    actualizar_estado(solicitud_id, estado, notas)
    solicitudes = obtener_solicitudes()
    return templates.TemplateResponse("partials/tabla_solicitudes.html", {
        "request": request,
        "solicitudes": solicitudes
    })


@app.get("/api/tiendas")
async def api_tiendas():
    """API endpoint for stores autocomplete."""
    return obtener_tiendas()


@app.get("/api/cargos")
async def api_cargos():
    """API endpoint for SSMM positions."""
    return obtener_cargos_ssmm()
