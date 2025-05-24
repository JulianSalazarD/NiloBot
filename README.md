# NiloBot APP

- **description**="Chatbot inteligente para análisis de facturación y nómina electrónica.",
- **version**="0.0.1"

Chatbot inteligente hackathon talentotech

## Integrantes

- Daniel Mazo
- Robin Cardenas
- Veronica Moreno
- Daniela Muñoz
- Julian Salazar

## Caracteristicas principales

- Procesamiento de Lenguaje Natural (NLP): Convierte tus preguntas en lenguaje natural en consultas SQL complejas.
- Integración con MariaDB: Conecta y extrae información directamente de tu base de datos MariaDB.
- Potenciado por Google Gemini: Utiliza la capacidad avanzada de Gemini para entender, razonar y generar respuestas.
- Respuestas Amigables: Un segundo LLM se encarga de transformar las respuestas técnicas de la base de datos en mensajes concisos y fáciles de entender para el usuario.
- API REST: Expone un endpoint HTTP para integrar el chatbot en cualquier aplicación externa.

## Tecnologias principales

- Python 3.13 +
- **FastAPI:** Framework web para construir la API REST.
- **LangChain:** Orquestación de LLMs, agentes y herramientas para interacción con bases de datos.
- **Google Gemini (vía langchain-google-genai):** Modelos de lenguaje grandes para el procesamiento de lenguaje natural y la generación de SQL/respuestas.
- **mysql-connector-python:** Driver de Python para conectar con la bases de dato.
- **python-dotenv:** Para la gestión segura de variables de entorno.
- **httpx:** Cliente HTTP asíncrono para interactuar con la API.
- **ngrok:** (Para desarrollo) Herramienta para exponer tu servidor local a Internet y probar webhooks.

## Guia de inicio rapido

Sigue estos pasos para poner a funcionar NiloBot en tu entorno local.

### 1. Clonar el Repositorio

### 2. Configuración del Entorno Virtual (Recomendado)

```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

En .env

```
# .env

# --- Google Gemini API Key ---
# Obtén tu clave en Google AI Studio: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY="TU_API_KEY_DE_GEMINI_AQUI"

# --- Database Connection ---
# Formato: mysql+mysqlconnector://usuario:contraseña@host:puerto/nombre_base_de_datos
# Ejemplo: mysql+mysqlconnector://admin:password@localhost:3306/mi_empresa_db
DATABASE_URL="mysql+mysqlconnector://tu_usuario:tu_password@tu_host:3306/nombre_de_tu_db"
```

**Importante:** Asegúrate de reemplazar los valores placeholder con tus credenciales reales.

## 5. Preparar tu Base de Datos Maria

Asegúrate de que tu base de datos esté funcionando y accesible desde tu_host:3306 (o el puerto que uses). La estructura de las tablas (esquema) en tu base de datos es crucial, ya que el chatbot la usará para generar consultas SQL. NiloBot introspectará automáticamente todas las tablas disponibles en la nombre_de_tu_db especificada.

## 6. Ejecutar la Aplicación FastAPI

Desde la raíz de tu proyecto, inicia el servidor FastAPI.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Pruebas y Uso

1. Probar la Conexión a la Base de Datos

Puedes verificar que NiloBot se conecta a tu base de datos y lee el esquema ejecutando directamente el script de conexión:

```Bash

python database/connection.py
```

Deberías ver mensajes de "Conexión a la base de datos exitosa" y una parte del esquema.
2. Probar la API REST del Chatbot

Accede a la documentación interactiva de FastAPI en tu navegador:

http://127.0.0.1:8000/docs

Aquí podrás probar el endpoint /chat enviando mensajes y viendo las respuestas de tu chatbot.
3.  exponer tu servidor a Internet

- Iniciar ngrok

En una nueva terminal (mientras FastAPI sigue ejecutándose), navega a la carpeta donde descomprimiste ngrok y ejecútalo para exponer el puerto 8000:
Bash

```
./ngrok http 8000   # macOS/Linux
ngrok http 8000     # Windows
```

ngrok te proporcionará una URL HTTPS pública temporal (ej., https://tu-id-aleatorio.ngrok-free.app). Cópiala, esta será tu NGROK_PUBLIC_URL.
