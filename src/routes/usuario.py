from flask import Blueprint, request, jsonify
from src.models.usuario import Usuario, db

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuario.get_all()
        return jsonify([usuario.serialize() for usuario in usuarios]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@usuario_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.json
    nombre = data.get('nombre')
    telefono = data.get('telefono')
    direccion = data.get('direccion')
    codigo = data.get('codigo')
    correo = data.get('correo')
    password = data.get('password')

    if not nombre or not telefono or not direccion or not codigo or not correo or not password:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        usuario = Usuario.create(nombre=nombre, telefono=telefono, direccion=direccion, codigo=codigo, correo=correo, password=password)
        return jsonify({'message': 'Usuario creado exitosamente', 'usuario': usuario.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear usuario: {str(e)}'}), 500
