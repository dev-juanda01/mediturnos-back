from flask import Blueprint, request, jsonify
from src.models.drogueria import Drogueria, db


drogueria_bp = Blueprint('drogueria_bp', __name__)

@drogueria_bp.route('/droguerias', methods=['GET'])
def get_droguerias():
    try:
        droguerias = Drogueria.query.all()
        return jsonify([drogueria.serialize() for drogueria in droguerias]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@drogueria_bp.route('/droguerias', methods=['POST'])
def create_drogueria():
    data = request.json
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    codigo = data.get('codigo')

    if not nombre or not direccion or not codigo:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        drogueria = Drogueria(nombre=nombre, direccion=direccion, codigo=codigo)
        db.session.add(drogueria)
        db.session.commit()
        return jsonify({'message': 'Droguería creada exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear droguería: {str(e)}'}), 500
