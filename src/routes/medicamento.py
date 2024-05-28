from flask import Blueprint, request, jsonify
from src.models.medicamento import Medicamento, db

# Definición del blueprint para medicamentos
medicamento_bp = Blueprint('medicamento_bp', __name__)

# Endpoint para obtener todos los medicamentos
@medicamento_bp.route('/medicamentos', methods=['GET'])
def get_medicamentos():
    try:
        medicamentos = Medicamento.get_all()
        return jsonify([medicamento.serialize() for medicamento in medicamentos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para crear un nuevo medicamento
@medicamento_bp.route('/medicamentos', methods=['POST'])
def create_medicamento():
    data = request.json
    nombre = data.get('nombre')
    codigo = data.get('codigo')
    stock = data.get('stock')
    laboratorio = data.get('laboratorio')
    dosis_medica = data.get('dosis_medica')
    concentracion = data.get('concentracion')
    presentacion = data.get('presentacion')
    tipo = data.get('tipo')

    # Validación de datos requeridos
    if not nombre or not codigo or not stock or not laboratorio or not dosis_medica or not concentracion or not presentacion or not tipo:
        return jsonify({'message': 'Faltan datos'}), 400

    # Crear el medicamento en la base de datos
    try:
        medicamento = Medicamento.create(
            nombre=nombre, codigo=codigo, stock=stock, laboratorio=laboratorio,
            dosis_medica=dosis_medica, concentracion=concentracion,
            presentacion=presentacion, tipo=tipo
        )
        return jsonify({'message': 'Medicamento creado exitosamente', 'medicamento': medicamento.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear medicamento: {str(e)}'}), 500