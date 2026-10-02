"""
Script principal para instancia y ejecutar el agente React utilizando Google AI.
"""

import os
from dotenv import load_dotenv

#importamos el conectpr de Google GenAi para LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from langchain_core.prompts import PromptTemplate

# Importamos la lista de herramientas desde nuestro modulo local
from tools import HERRAMIENTAS_AGENTE

#1. Cargar las variables de entorno desde el archivo .env
load_dotenv()

def inicializar_agente():
    # Validar que la API key de Google esté presente en las variables de entorno
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("La variable de entorno GOOGLE_API_KEY no está definida. Por favor, configúrala en el archivo .env.")

    # 2. Inicializar el modelo de lenguaje de Google Generative AI
    llm = ChatGoogleGenerativeAI(
        model = "gemini-3.8-flash",
        temperature = 0, 
        google_api_key = os.getenv("GOOGLE_API_KEY")
    )

    # 3. Crearl prompt de ReAct
    prompt = PromptTemplate.from_template("""
        You are an assistant that calculates subscription prices.

        You have access to the following tools:

        {tools}

        Use the following format:

        Question: the user's question
        Thought: think about what you need to do
        Action: the action to take, must be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ...
        Final Answer: the final answer

        IMPORTANT:
        - When a tool has one argument, pass only the value of that argument.
        - For calcular_descuento_volumen, Action Input must be the number of users, such as 45.
        - For obtener_tarifa_base, Action Input must be the plan name, such as pro.
        - Do not invent tool names.

        Question: {input}
        Thought:{agent_scratchpad}
        """)

    # 4. Crear la estructura del agente ReAct con las herramientas y el prompt
    agent = create_react_agent(
        llm = llm,
        tools = HERRAMIENTAS_AGENTE,
        prompt = prompt
    )

    # 5. Crear un ejecutor de agente para manejar la interacción (AgentExecutor)
    agent_executor = AgentExecutor(
        agent = agent,
        tools = HERRAMIENTAS_AGENTE,
        verbose = True, #Muestra el razonamiento paso a paso
        handle_parsing_errors = True,
        max_iterations = 5
    )

    return agent_executor

def main():
    print( "Inicializando el agente ReAct con Google AI...")
    agente = inicializar_agente()

    prompt_usuario = (
        "Necesito un presupuesto para 45 usuarios en el plan 'Pro' contratado "
        "por un año completo (12 meses). ¿Cuál es el coste total anual aplicando "
        "los descuentos correspondientes?"
    )

    print(f"\nPregunta del usuario:\n{prompt_usuario}\n")
    print("--- INICIO DE LA TRAZA DE RAZONAMIENTO DEL AGENTE ---\n")

    #Ejecutamos el agente
    respuesta = agente.invoke({"input": prompt_usuario})

    print("\n--- FIN DE LA TRAZA DE RAZONAMIENTO DEL AGENTE ---\n")
    print(f"Respuesta del agente:\n{respuesta['output']}")


if __name__ == "__main__":
    main()