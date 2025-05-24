
import os
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Variable global para almacenar la instancia de la conexión a la base de datos
_db_instance = None

def get_db_connection() -> SQLDatabase:
    """
    Retorna una instancia singleton de SQLDatabase de LangChain,
    configurada para introspectar todas las tablas.

    Esta función asegura que solo exista una conexión a la base de datos
    durante la ejecución del programa. Utiliza una variable global `_db_instance`
    para mantener la instancia de la conexión.

    Returns:
        SQLDatabase: Una instancia de SQLDatabase configurada para interactuar
        con la base de datos especificada en la variable de entorno DATABASE_URL.

    Raises:
        ValueError: Si la variable de entorno DATABASE_URL no está definida.
        Exception: Si ocurre un error al conectar o introspectar la base de datos.
    """
    global _db_instance
    if _db_instance is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL no está definida en las variables de entorno.")

        try:
            engine = create_engine(database_url)
            _db_instance = SQLDatabase(engine)
            print(f"Conexión a la base de datos '{database_url}' exitosa.")
            print("Esquema de la base de datos (todas las tablas accesibles) cargado por LangChain.")
            print(f"Tablas introspectadas: {_db_instance.get_usable_table_names()}")

        except Exception as e:
            print(f"Error al conectar o introspectar la base de datos: {e}")
            print("Asegúrate de que la cadena de conexión sea correcta y los drivers de DB estén instalados.")
            raise

    return _db_instance

def test_db_connection():
    """
    Prueba la conexión a la base de datos y muestra una parte del esquema.
    Ejecutar directamente este archivo para probar: python -m database.connection

    Esta función obtiene una conexión a la base de datos utilizando `get_db_connection()`
    y luego imprime una vista del esquema de la base de datos (los primeros 500 caracteres).
    Esto permite verificar que la conexión a la base de datos está funcionando correctamente
    y que el esquema se puede leer.
    """
    try:
        db = get_db_connection()
        print("\n--- Vista del Esquema de la Base de Datos (Primeras 500 caracteres) ---")
        full_schema_info = db.get_table_info()
        print(full_schema_info[:500] + "..." if len(full_schema_info) > 500 else full_schema_info)
        print("\nEl LLM recibirá esta información de esquema como contexto.")
    except Exception as e:
        print(f"La prueba de conexión falló: {e}")

# Esto permite ejecutar `python database/connection.py` para probar solo la conexión
if __name__ == "__main__":
    test_db_connection()