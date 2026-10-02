"""
Módulo de herramientas (Tools) utilizados por el Agente React.
Cada función decorada con @tool debe incluir anotaciones de tipo y un docstring descriptivo que el LLM usará para razonar.
"""

from langchain_core.tools import tool

@tool
def obtener_tarifa_base(plan: str) -> float:
    """Devuelve la tarifa base mensual por usuario en euros según el tipo de plan."""
    tarifas = {
        "basic": 10.0,
        "pro": 25.0,
        "enterprise": 50.0
    }

    plan_clean = str(plan).lower().strip()
    return tarifas.get(plan_clean, 0.0)


@tool
def calcular_descuento_volumen(numero_usuarios: int) -> float:
    """Calcula el porcentaje de descuento según el número de usuarios."""
    try:
        numero_usuarios = int(numero_usuarios)
    except (TypeError, ValueError):
        raise ValueError("numero_usuarios debe ser un número entero"
    )

    if numero_usuarios >= 100:
        return 0.20
    elif numero_usuarios >= 20:
        return 0.10
    else:
        return 0.0



# ==============================================================================================
# LISTA EXPORTABLE DE HERRAMIENTAS
# Esta es la variable que importa main.py (from tools import HERRAMIENTAS_AGENTE) para pasarla al agente ReAct.
# ==============================================================================================
HERRAMIENTAS_AGENTE = [
    obtener_tarifa_base,
    calcular_descuento_volumen
]