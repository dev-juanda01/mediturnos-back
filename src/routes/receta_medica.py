from flask import Blueprint, request, jsonify
from src.models.receta_medica import RecetaMedica, db
from datetime import datetime
import pytz

# Definición del blueprint para recetas médicas
receta_medica_bp = Blueprint('receta_medica_bp', __name__)

# Endpoint para obtener todas las recetas médicas almacenadas
@receta_medica_bp.route('/recetas-medicas', methods=['GET'])
def get_recetas_medicas():
    try:
        recetas = RecetaMedica.get_all()
        return jsonify([receta.serialize() for receta in recetas]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para crear una nueva receta médica
@receta_medica_bp.route('/recetas-medicas', methods=['POST'])
def create_receta_medica():
    data = request.json
    id_paciente = data.get('id_paciente')
    id_eps = data.get('id_eps')
    medico = data.get('medico')
    id_medicamento = data.get('id_medicamento')
    fecha_str = data.get('fecha')
    codigo = data.get('codigo')

    # Valida que todos los datos estén
    if not id_paciente or not id_eps or not medico or not id_medicamento or not fecha_str or not codigo:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        # Convertir fecha_str a objeto datetime
        local_tz = pytz.timezone('America/Bogota')
        fecha = local_tz.localize(datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S'))

         # Crear la receta médica en la base de datos
        receta = RecetaMedica.create(
            id_paciente=id_paciente, id_eps=id_eps, medico=medico,
            id_medicamento=id_medicamento, fecha=fecha, codigo=codigo
        )
        return jsonify({'message': 'Receta médica creada exitosamente', 'receta': receta.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear receta médica: {str(e)}'}), 500
