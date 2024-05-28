from flask import Blueprint, request, jsonify
from src.models.paciente import Paciente, db


# Definición del blueprint para pacientes
paciente_bp = Blueprint('paciente_bp', __name__)

# Endpoint para obtener todos los pacientes
@paciente_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        pacientes = Paciente.get_all()
        return jsonify([paciente.serialize() for paciente in pacientes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para crear un nuevo paciente
@paciente_bp.route('/pacientes', methods=['POST'])
def create_paciente():
    data = request.json
    nombre = data.get('nombre')
    documento = data.get('documento')
    tipo_documento = data.get('tipo_documento')
    eps = data.get('eps')
    telefono = data.get('telefono')
    correo = data.get('correo')

    # Valida que todos los campos necesarios estén
    if not nombre or not documento or not tipo_documento or not eps or not telefono or not correo:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        # Crea un nuevo paciente y lo guarda en la base de datos
        paciente = Paciente.create(nombre=nombre, documento=documento, tipo_documento=tipo_documento, eps=eps, telefono=telefono, correo=correo)
        return jsonify({'message': 'Paciente creado exitosamente', 'paciente': paciente.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear paciente: {str(e)}'}), 500