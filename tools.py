"""
Tools used by the subscription pricing agent.

Each function decorated with @tool becomes available
to the LangChain agent.
"""

from langchain_core.tools import tool


@tool
def obtener_tarifa_base(plan: str) -> float:
    """
    Return the monthly base price per user in euros
    for the specified subscription plan.
    """

    tarifas = {
        "basic": 10.0,
        "pro": 25.0,
        "enterprise": 50.0,
    }

    plan_clean = str(plan).lower().strip()

    if plan_clean not in tarifas:
        raise ValueError(
            f"Plan desconocido: '{plan}'. "
            f"Planes disponibles: {', '.join(tarifas.keys())}."
        )

    return tarifas[plan_clean]


@tool
def calcular_descuento_volumen(numero_usuarios: int) -> float:
    """
    Return the volume discount percentage based
    on the number of users.
    """

    try:
        numero_usuarios = int(numero_usuarios)
    except (TypeError, ValueError):
        raise ValueError(
            "numero_usuarios debe ser un número entero."
        )

    if numero_usuarios < 1:
        raise ValueError(
            "numero_usuarios debe ser mayor que cero."
        )

    if numero_usuarios >= 100:
        return 0.20

    if numero_usuarios >= 20:
        return 0.10

    return 0.0


# Tools exposed to the agent
HERRAMIENTAS_AGENTE = [
    obtener_tarifa_base,
    calcular_descuento_volumen,
]
