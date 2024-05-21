from flask import Flask, jsonify
from src.routes.drogueria import drogueria_bp
from src.routes.usuario import usuario_bp
from src.routes.paciente import paciente_bp
from src.routes.medicamento import medicamento_bp
from src.routes.receta_medica import receta_medica_bp
from config import Config
from src.models.drogueria import db

# Crear instancia de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Ruta de bienvenida
@app.route('/')
def index():
    return jsonify({'message': 'Bienvenido a la API de MediTurnos'})

# Registrar el blueprint con el prefijo '/api'
app.register_blueprint(drogueria_bp, url_prefix='/api')
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(paciente_bp, url_prefix='/api')
app.register_blueprint(medicamento_bp, url_prefix='/api')
app.register_blueprint(receta_medica_bp, url_prefix='/api')

# Inicializar la base de datos SQLAlchemy
db.init_app(app)

# Correr la aplicación
if __name__ == "__main__":
    app.run(debug=True, port=5000)
