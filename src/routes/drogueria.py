import mysql.connector
from config import Config
from flask import Blueprint, request, jsonify
from src.models.drogueria import Drogueria

drogueria_bp = Blueprint('drogueria_bp', __name__)

@drogueria_bp.route('/droguerias', methods=['GET'])
def get_droguerias():
    droguerias = Drogueria.get_all()
    return jsonify(droguerias)

@drogueria_bp.route('/droguerias', methods=['POST'])
def create_drogueria():
    data = request.json
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    codigo = data.get('codigo')
    if Drogueria.create(nombre, direccion, codigo):
        return jsonify({'message': 'Droguería creada exitosamente'}), 201
    return jsonify({'message': 'Error al crear la droguería'}), 500
