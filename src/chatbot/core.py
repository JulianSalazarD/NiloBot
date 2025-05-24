import os
import sys
import datetime
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from database.connection import get_db_connection
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Mantener una única instancia del agente
_agent_executor: AgentExecutor | None = None
# Nuevo LLM para respuestas amigables
_friendly_llm: ChatGoogleGenerativeAI | None = None 

def create_gemini_sql_agent(db) -> AgentExecutor:
    """
    Configura y retorna el agente de LangChain con Google Gemini y la base de datos.

    Args:
        db (SQLDatabase): Una instancia de SQLDatabase conectada a la base de datos.

    Returns:
        AgentExecutor: Un agente configurado para interactuar con la base de datos
                       utilizando el modelo Gemini.

    Raises:
        ValueError: Si la variable de entorno GOOGLE_API_KEY no está definida.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY no está definida en las variables de entorno.")


    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1,
        google_api_key=google_api_key
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent_executor


async def get_chatbot_response(message: str) -> str:
    """
    Procesa el mensaje del usuario, genera y ejecuta la consulta SQL,
    y devuelve la respuesta del chatbot utilizando el agente global.

    Args:
        message (str): El mensaje del usuario.

    Returns:
        str: Una respuesta amigable y concisa para el usuario,
             generada a partir de la respuesta de la base de datos.

    Raises:
        ValueError: Si la variable de entorno GOOGLE_API_KEY no está definida.
        Exception: Si ocurre un error al invocar el agente del chatbot
                   o al generar la respuesta amigable.
    """
    global _agent_executor, _friendly_llm
    if _agent_executor is None:
        from database.connection import get_db_connection
        db_instance = get_db_connection()
        _agent_executor = create_gemini_sql_agent(db_instance)

    # LLM para respuestas amigavles
    if _friendly_llm is None:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY no está definida en las variables de entorno.")
        _friendly_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7, # Un poco más de creatividad para la amabilidad
            google_api_key=google_api_key
        )

    # Obtener la fecha actual
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    date_context = (
        f"Contexto de fecha actual: El año actual es {today.year}, "
        f"el mes actual es {today.month}, el día actual es {today.day}. "
        "Ten esto en cuenta para consultas sobre 'este mes', 'este año', 'hoy', 'el mes pasado', etc."
    )
    prompt_with_date_context = f"{date_context}\n\nPregunta del usuario: {message}"

    
    try:
        response = await _agent_executor.ainvoke({"input": prompt_with_date_context})
        print(f"--- Respuesta del Agente: {response['output']} ---")
    except Exception as e:
        print(f"Error al invocar el agente del chatbot: {e}")
        return "Lo siento, no pude procesar tu solicitud en este momento. ¿Podrías reformularla?"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "Eres un asistente amigable y conciso. Tu tarea es tomar la pregunta original del usuario "
            "y la respuesta detallada generada por un sistema de consultas a base de datos, "
            "y transformarla en una respuesta corta, amigable y fácil de entender para el usuario final. "
            "Si la respuesta de la base de datos es una cifra monetaria, asegúrate de formatearla con el símbolo '$' y comas para miles. "
            "Si el resultado no es un número, resúmelo de forma clara. "
            "Finaliza siempre con una pregunta que invite a continuar la conversación, como '¿Hay algo más en lo que pueda ayudarte?' o '¿Necesitas otra consulta?'."
            "asegurate que la respuesta sea en español"
            "Si el input no está en la base de datos o no es una consulta como, hola, como estas?, responde de manera amigable"
        )),
        ("human", (
            "Pregunta original del usuario: {message}\n\n"
            "Respuesta detallada de la base de datos: {sql_agent_response}"
        ))
    ])

    # Construir el prompt con la información
    formatted_prompt = prompt_template.format_messages(
        message=message,
        sql_agent_response=response['output']
    )

    friendly_response = ""
    try:
        print(f"\n--- Generador de Respuesta Amigable: Reformulando respuesta ---")
        llm_response = await _friendly_llm.ainvoke(formatted_prompt)
        friendly_response = llm_response.content
        print(f"--- Generador de Respuesta Amigable: Respuesta final: {friendly_response} ---\n")
    except Exception as e:
        print(f"❌ Error al generar respuesta amigable: {e}")
        # Si falla el reformateo, al menos devolvemos la respuesta bruta del agente SQL
        return sql_agent_raw_response + " (No pude reformular la respuesta amistosamente, lo siento)."

    return friendly_response