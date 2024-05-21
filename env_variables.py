import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

envs = {
    "DATABASE_URI": os.getenv("SQLALCHEMY_DATABASE_URI"),
    "TRACK_MODIFICATIONS": eval(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
}