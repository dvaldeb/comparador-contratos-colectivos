"""Datos v6 - Corregido: colaboradores, ortografia, traducciones."""

PRIMER_DIA = {
    "bienvenida": "Hoy empiezas una aventura increíble. No te preocupes si al principio suena a sopa de letras... ¡a todos nos pasó!",
    "tips": [
        ("Pregunta sin miedo", "La Puerta Abierta existe para eso."),
        ("Las siglas se aprenden", "En 2 semanas ya las manejas."),
        ("Recorre tu tienda/oficina", "Entiende cómo fluye todo."),
        ("Tu opinión importa", "Las ideas frescas son bienvenidas."),
    ],
    "no_asustes": [
        "No entiendes una sigla en reunión",
        "Te pierdes en la tienda",
        "La bodega parece un laberinto",
        "Escuchas 'apantallar' por primera vez",
    ],
    "sabias_que": [
        "Walmart tiene ~2.1 millones de colaboradores en el mundo",
        "Sam Walton abrió la 1era tienda en 1962 en Arkansas",
        "Walmart Chile es el supermercado #1 del país",
        "No hay 'empleados', todos somos 'colaboradores'",
    ],
}

WALMART_GLOBAL = {
    "fundacion": "1962, Rogers, Arkansas",
    "colaboradores_global": "~2.1 millones",
    "fortune500": "#1 Fortune 500",
    "tiendas_intl": "5,400+ tiendas",
    "creencias": [
        ("Respeto por el Individuo", "Cada persona es única y valiosa"),
        ("Servicio al Cliente", '"Solo hay un jefe... el cliente"'),
        ("Búsqueda de la Excelencia", "Superar el miedo al fracaso"),
    ],
    "mercados": "México, Canadá, Chile, China, India, Sudáfrica",
}

WALMART_CHILE = {
    "historia": "Walmart adquirió D&S en 2008-2009. Así nació Walmart Chile.",
    "competencia": [
        ("Cencosud", "Jumbo, Santa Isabel"),
        ("Falabella", "Tottus, Sodimac"),
        ("SMU", "Unimarc"),
        ("MercadoLibre", "Crecimiento 71%"),
    ],
    "prioridades": [
        ("Win in Omni (Ganar en Omnicanal)", "20% penetración online"),
        ("Run Great Stores (Operar Grandes Tiendas)", "Simplificar operación"),
        ("Develop Ecosystem (Desarrollar Ecosistema)", "Mi Club 3.2M MAU"),
        ("Marketplace (Mercado en línea)", "2M SKUs en 3P"),
        ("Mayorista Digital", "#2 B2B Chile"),
        ("Talent (Talento)", "Mentalidad digital"),
        ("Power Tech (Potenciar Tecnología)", "Reducir deuda técnica"),
    ],
    "sociedades": [
        ("S150", "Líder"), ("S151", "Express"), ("S260", "Express 400"),
        ("S107", "SBA/Acuenta"), ("S157", "Mayorista"),
    ],
}

FORMATOS = [
    {"nombre": "Líder (Híper)", "tipo": "Hipermercado", "desc": "Tienda grande con TODO. Banner #1 Chile.", "nps": ">= 65%", "sap": "S150"},
    {"nombre": "Express", "tipo": "Supermercado urbano", "desc": "Compra rápida cerca de casa.", "nps": ">= 63%", "sap": "S151"},
    {"nombre": "aCuenta (SBA)", "tipo": "Bodega descuento", "desc": "Los MEJORES precios. Sin lujos.", "nps": ">= 78%", "sap": "S107"},
    {"nombre": "Mayorista", "tipo": "B2B Mayorista", "desc": "Para negocios. 13 tiendas.", "nps": ">= 70%", "sap": "S157"},
    {"nombre": "Ekono / Express 400", "tipo": "Barrio (phase out / en cierre)", "desc": "En proceso de cierre.", "nps": "-", "sap": "S260"},
]

MARCAS = [
    ("Great Value (Gran Valor)", "Alimentos y hogar"),
    ("Equate", "Salud y belleza"),
    ("Mainstays (Esenciales)", "Hogar y decoración"),
    ("Acuenta", "Valor / Descuento"),
    ("Líder (marca)", "Multicategoría"),
    ("Spark Create Imagine", "Bebés y niños"),
]

SERVICIOS = [
    ("Presto", "Tarjeta de crédito propia"),
    ("MasterCard Presto", "Tarjeta co-branded (marca compartida)"),
    ("Mi Club", "Fidelización 3.2M MAU (usuarios activos mensuales)"),
    ("Créditos / Seguros", "Financiamiento"),
]

# KPIs - título, resumen ejecutivo, términos (máx 4 por slide)
KPIS = [
    {
        "titulo": "Personas y Productividad",
        "resumen": "Miden si tenemos la gente correcta en el lugar correcto y cuán eficientes somos.",
        "terms": [
            ("UPLH", "Units Per Labor Hour (Unidades por Hora Trabajada)", "Unidades vendidas por hora trabajada. EL indicador de productividad."),
            ("JEQ", "Jornada Equivalente", "1 JEQ = 176 hrs/mes. Media jornada = 0.5 JEQ."),
            ("Ausentismo", "% Ausencias", "Verde <= 10% | Amarillo 10-20% | Rojo > 20%"),
            ("Rotación", "Turnover (Tasa de Salida)", "% colaboradores que se van vs activos. Mensual."),
        ]
    },
    {
        "titulo": "NPS y Satisfacción",
        "resumen": "El termómetro de la experiencia del cliente. Se mide vía Medallia.",
        "terms": [
            ("NPS", "Net Promoter Score (Índice de Recomendación)", "Cuánto nos recomienda el cliente (0-10)."),
            ("NPS Físico", "En tienda", "Se actualiza semanalmente, los martes."),
            ("NPS Digital", "Canal online (en línea)", "Target >= 49%. Rojo < 44%."),
            ("CSAT", "Customer Satisfaction (Satisfacción del Cliente)", "Por atributo (1-7). Explica el NPS."),
        ]
    },
    {
        "titulo": "Ventas y Finanzas",
        "resumen": "La salud financiera del negocio. Estos números definen si cumplimos metas.",
        "terms": [
            ("Venta Neta", "Net Sales (Ventas Netas)", "Cuánto vendimos. LA métrica reina."),
            ("Comp", "Comparable Sales (Ventas Comparables)", "Crecimiento vs mismo período año anterior."),
            ("Ticket Promedio", "Avg Ticket (Boleta Promedio)", "Cuánto gasta cada cliente por visita."),
            ("GMV", "Gross Merch. Value (Valor Bruto de Mercancía)", "Venta bruta tiendas + eComm + MKP."),
        ]
    },
    {
        "titulo": "Góndola e Instock",
        "resumen": "Si no está en góndola, no se vende. Aseguran que el cliente encuentre lo que busca.",
        "terms": [
            ("NSG", "Nivel Servicio Góndola", "Disponible, ordenado, limpio, con fleje. Verde >= 97.5%"),
            ("Instock", "% En Stock (% en Existencia)", "Producto vs demanda. Verde >= 96%."),
            ("DOH", "Days on Hand (Días de Inventario)", "Días de stock. Verde >= 10, Rojo < 6."),
            ("Quiebre", "Stockout (Falta de Stock)", "No hay producto en góndola. Enemigo #1."),
        ]
    },
    {
        "titulo": "Merma y Pérdidas",
        "resumen": "Cada producto dañado, vencido o hurtado impacta el resultado directo.",
        "terms": [
            ("Desecho", "Waste (Desperdicio)", "Productos vencidos o mal etiquetados."),
            ("Dañado", "Damaged (Producto Dañado)", "Productos que ya no se pueden vender."),
            ("Fresh Loss", "Pérdida Frescos", "(Desecho + Desconocido) / Venta."),
            ("Proy. Inventario", "Projected Loss (Pérdida Proyectada)", "Pérdida estimada desde último conteo."),
        ]
    },
    {
        "titulo": "Checkout y Pago",
        "resumen": "Nadie quiere esperar en la fila. Miden la rapidez del proceso de pago.",
        "terms": [
            ("NTC", "Nivel Tiempo Caja", "Líder >= 81% | Express >= 80% | SBA >= 82%."),
            ("Uso SCO", "Self-Checkout (Caja de Autoservicio)", "Líder >= 24% | Express >= 35% | SBA >= 25%."),
            ("NSC", "Nivel Serv. Checkout (Nivel Servicio Caja)", "% tiempo sin cola. Verde >= 80%."),
            ("Pedido Perfecto", "OTIF: On-Time, In-Full (A Tiempo y Completo)", "Verde >= 40%."),
        ]
    },
]

# Glosario - resúmenes ejecutivos, máx 4 por slide
GLOSARIO = [
    {
        "titulo": "Tienda y Sala",
        "resumen": "El vocabulario básico para entender cómo funciona una tienda.",
        "color": "blue",
        "terms": [
            ("Góndola", "Las estanterías con productos en los pasillos."),
            ("Planograma", "El 'mapa' de qué producto va en qué lugar."),
            ("Fleje", "Etiqueta de precio en góndola. PLU + precio."),
            ("Cabecera", "Punta de góndola. Espacio VIP para promociones."),
        ]
    },
    {
        "titulo": "Tienda y Sala (2)",
        "resumen": "Más términos que escucharás en tu día a día.",
        "color": "blue",
        "terms": [
            ("Apantallar", "Poner productos 'bonitos' al frente con bajo stock."),
            ("Beta / Gamma", "Beta = entrada clientes. Gamma = entrada colaboradores."),
            ("POS", "Point of Sale (Punto de Venta). La caja registradora."),
            ("Regla 4x1", "Revisar: fleje, limpieza, presentación, quiebres."),
        ]
    },
    {
        "titulo": "Inventario y Stock (Existencias)",
        "resumen": "Cómo controlamos la mercadería de principio a fin.",
        "color": "purple",
        "terms": [
            ("PLU", "Price Look-Up (Código de Precio). El 'RUT' del producto."),
            ("SKU / UPC", "Stock Keeping Unit / Universal Product Code (Código de Producto / Código de Barra)."),
            ("FIFO / FEFO", "First In First Out / First Expired First Out (Primero en Entrar, Primero en Salir / Primero en Vencer, Primero en Salir)."),
            ("Bin", "Ubicación codificada en bodega."),
        ]
    },
    {
        "titulo": "E-Commerce y Digital (Comercio Electrónico)",
        "resumen": "El mundo online. Cada vez más clientes compran desde el celular.",
        "color": "cyan",
        "terms": [
            ("Lider.cl / LiderApp", "Nuestra tienda online (en línea) y app móvil."),
            ("SOD", "Supermercado On Demand (Bajo Demanda). Online con stock de tienda."),
            ("DarkStore", "Tienda Oscura: solo para pedidos online. Sin clientes."),
            ("1P / 3P", "1P = Walmart vende. 3P = Seller externo (vendedor externo)."),
        ]
    },
    {
        "titulo": "Fulfillment y Logística (Cumplimiento de Pedidos)",
        "resumen": "Desde que el cliente hace click hasta que recibe su pedido.",
        "color": "orange",
        "terms": [
            ("Picking (Recolección)", "Armar el pedido recorriendo la tienda."),
            ("Home Delivery (Despacho a Domicilio)", "Despacho a la puerta de tu casa."),
            ("Pickup (Retiro en Tienda)", "Compras online, retiras en tienda."),
            ("LAT", "Líder al Toque. Despacho MISMO DÍA."),
        ]
    },
    {
        "titulo": "Tecnología",
        "resumen": "Los sistemas que hacen funcionar todo detrás de escena.",
        "color": "indigo",
        "terms": [
            ("IMS (Wakanda)", "Inventory Management System (Sistema de Inventario). Sí, se llama Wakanda."),
            ("WMS (Dr Strange)", "Warehouse Management System (Sistema de Bodega). Los nombres Marvel son tradición."),
            ("OMS", "Order Management System (Sistema de Gestión de Pedidos). Ciclo de vida de pedidos online."),
            ("SAP", "El cerebro administrativo: finanzas, RRHH, supply chain (cadena de suministro)."),
        ]
    },
    {
        "titulo": "Finanzas y Compras",
        "resumen": "Cómo decidimos qué vender, a qué precio y si funcionó.",
        "color": "teal",
        "terms": [
            ("CATMAN", "Category Management (Gestión de Categorías). Qué productos van en tienda."),
            ("Rollback (Rebaja Temporal)", "Baja temporal de precio. Clásico de Walmart."),
            ("Markdown (Rebaja)", "Rebaja para liquidar stock (existencias)."),
            ("Sell-through (Venta Efectiva)", "% vendido vs recibido. Velocidad de venta."),
        ]
    },
]
