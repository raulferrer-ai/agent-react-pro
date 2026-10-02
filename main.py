"""
Main application for the subscription pricing AI agent.

The agent uses LangChain's current create_agent API and
Google Gemini to decide which tools to call.
"""

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import HERRAMIENTAS_AGENTE


def inicializar_agente():
    """
    Create and configure the subscription pricing agent.
    """

    # Load environment variables from .env
    load_dotenv()

    # Validate Google API key
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        raise ValueError(
            "La variable de entorno GOOGLE_API_KEY no está definida. "
            "Configúrala en el archivo .env."
        )

    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        google_api_key=google_api_key,
    )

    # System instructions for the agent
    system_prompt = """
You are an assistant that calculates subscription prices.

You have access to tools that provide:
- The monthly base price for a subscription plan.
- The volume discount based on the number of users.

Use the tools whenever you need pricing information.

Rules:
- Do not invent prices or discounts.
- Always use the appropriate tool to retrieve the base price.
- Always use the appropriate tool to calculate the volume discount.
- The plan name should be passed as a string, such as "pro".
- The number of users should be passed as an integer, such as 45.
- Explain the calculation clearly in the final answer.
- Include the monthly base price, number of users, discount,
  and final annual price when relevant.
"""

    # Create the agent
    agent = create_agent(
        model=llm,
        tools=HERRAMIENTAS_AGENTE,
        system_prompt=system_prompt,
        name="subscription_pricing_agent",
    )

    return agent


def main():
    print("Inicializando el agente de precios con Google Gemini...")

    agente = inicializar_agente()

    prompt_usuario = (
        "Necesito un presupuesto para 45 usuarios en el plan 'Pro' "
        "contratado por un año completo (12 meses). "
        "¿Cuál es el coste total anual aplicando los descuentos correspondientes?"
    )

    print("\nPregunta del usuario:")
    print(prompt_usuario)

    print("\n--- EJECUTANDO AGENTE ---\n")

    # Execute the agent
    respuesta = agente.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt_usuario,
                }
            ]
        }
    )

    print("\n--- FIN DE LA EJECUCIÓN ---\n")

    # The current create_agent API returns a message-based state.
    mensajes = respuesta["messages"]

    # The last message should contain the final AI response.
    mensaje_final = mensajes[-1]

    print("Respuesta del agente:")
    print(mensaje_final.content)


if __name__ == "__main__":
    main()
