from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Define la estructura de la solicitud de chat del usuario."""
    message: str # El mensaje que el usuario envía al chatbot

class ChatResponse(BaseModel):
    """Define la estructura de la respuesta que el chatbot envía al usuario."""
    response: str # La respuesta del chatbot


