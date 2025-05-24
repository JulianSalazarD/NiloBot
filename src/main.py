# nilobot_project/main.py
from fastapi import FastAPI, HTTPException, Request, Response, status
from dotenv import load_dotenv
import os



# Importa tus schemas para la validación de la API
from schemas.chatbot_schemas import ChatRequest, ChatResponse
# Importa la función principal de tu chatbot
from chatbot.core import get_chatbot_response

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="NiloBot API",
    description="Chatbot inteligente para análisis de facturación y nómina electrónica.",
    version="0.0.1"
)


# --- Endpoint para realizar consultas al chatbot ---
@app.post("/chat", response_model=ChatResponse, summary="Envía una pregunta al chatbot y recibe una respuesta.")
async def chat_with_nilobot(request: ChatRequest):
    """
    Este endpoint permite a cualquier cliente (ej. una aplicación web, móvil)
    enviar una pregunta en lenguaje natural al NiloBot y recibir una respuesta
    basada en los datos de facturación y nómina.
    """
    try:
        # Llama a la función principal del chatbot para obtener la respuesta
        response_content = await get_chatbot_response(request.message)
        # Retorna la respuesta en el formato definido por ChatResponse
        return ChatResponse(response=response_content)
    except Exception as e:
        # En caso de error, imprime un mensaje y lanza una excepción HTTP
        print(f"❌ Error en el endpoint /chat: {e}")
        raise HTTPException(status_code=500, detail="Lo siento, hubo un error procesando tu solicitud.")