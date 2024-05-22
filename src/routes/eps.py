from flask import Blueprint, request, jsonify
from src.models.eps import Eps, db

# Definir un Blueprint para las rutas de EPS
eps_bp = Blueprint('eps_bp', __name__)

@eps_bp.route('/eps', methods=['GET'])
def get_eps():
    try:
        eps_list = Eps.get_all()
        return jsonify([eps.serialize() for eps in eps_list]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@eps_bp.route('/eps', methods=['POST'])
def create_eps():
    data = request.json
    nombre = data.get('nombre')
    codigo = data.get('codigo')
    tipo = data.get('tipo')

    if not nombre or not codigo or not tipo:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        eps = Eps.create(nombre=nombre, codigo=codigo, tipo=tipo)
        return jsonify({'message': 'EPS creada exitosamente', 'eps': eps.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear EPS: {str(e)}'}), 500
