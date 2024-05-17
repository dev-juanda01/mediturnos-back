# importar paquete
from flask import Flask, jsonify
from config import Config
#from src.routes import drogueria
from src.routes.drogueria import drogueria_bp  # Importa el blueprint correcto



# crear instancia
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'message': 'Bienvenido a la API de MediTurnos'})

# Registrar el blueprint (si lo estás usando)
from src.routes.drogueria import drogueria_bp
app.register_blueprint(drogueria_bp, url_prefix='/api')

# correr aplicacion
if "__main__" == __name__:
    app.run(debug=True, port=5000)