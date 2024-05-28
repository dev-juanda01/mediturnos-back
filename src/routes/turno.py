from flask import Blueprint, request, jsonify
from src.models.turno import Turno, db
from datetime import datetime
import pytz

# Definición del blueprint para turnos
turno_bp = Blueprint('turno_bp', __name__)

# Endpoint para obtener todos los turnos
@turno_bp.route('/turnos', methods=['GET'])
def get_turnos():
    try:
        turnos = Turno.query.all()  # Usando SQLAlchemy para obtener todos los turnos
        return jsonify([turno.serialize() for turno in turnos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para crear un nuevo turno
@turno_bp.route('/turnos', methods=['POST'])
def create_turno():
    data = request.json
    id_drogueria = data.get('id_drogueria')
    la_receta_medica = data.get('la_receta_medica')
    id_usuario = data.get('id_usuario')
    estado = data.get('estado')
    tipo = data.get('tipo')
    fecha_asignacion_str = data.get('fecha_asignacion')
    fecha_finalizacion_str = data.get('fecha_finalizacion')
    novedades = data.get('novedades')
    limite_recetas = data.get('limite_recetas')

    # Valida que  todos los campos necesarios esten
    if not id_drogueria or not la_receta_medica or not id_usuario or not estado or not tipo or not fecha_asignacion_str or not limite_recetas:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        # Convertir fecha_asignacion_str y fecha_finalizacion_str a objetos datetime
        local_tz = pytz.timezone('America/Bogota')
        fecha_asignacion = local_tz.localize(datetime.strptime(fecha_asignacion_str, '%Y-%m-%d %H:%M:%S'))
        fecha_finalizacion = local_tz.localize(datetime.strptime(fecha_finalizacion_str, '%Y-%m-%d %H:%M:%S')) if fecha_finalizacion_str else None

        # Crear el turno usando SQLAlchemy
        turno = Turno.create(
            id_drogueria=id_drogueria, la_receta_medica=la_receta_medica, id_usuario=id_usuario,
            estado=estado, tipo=tipo, fecha_asignacion=fecha_asignacion,
            fecha_finalizacion=fecha_finalizacion, novedades=novedades, limite_recetas=limite_recetas
        )

        return jsonify({'message': 'Turno creado exitosamente', 'id_turno': turno.id_turno}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error al crear turno: {str(e)}'}), 500

# Endpoint para obtener el turno activo de un usuario específico
@turno_bp.route('/turnos/activo/<int:id_usuario>', methods=['GET'])
def get_active_turno_by_user(id_usuario):
    try:
        turno = Turno.get_active_turn_by_user(id_usuario)
        if turno:
            return jsonify(turno.serialize()), 200
        else:
            return jsonify({'message': 'No se encontró un turno activo para el usuario especificado'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al obtener el turno activo: {str(e)}'}), 500

# Endpoint para actualizar el estado de un turno específico
@turno_bp.route('/turnos/<int:id_turno>/estado', methods=['PUT'])
def update_turno_estado(id_turno):
    data = request.json
    nuevo_estado = data.get('estado')

    # Valida que el nuevo estado este presente en la solicitud
    if not nuevo_estado:
        return jsonify({'message': 'Falta el estado'}), 400

    try:
        turno = Turno.update_estado(id_turno, nuevo_estado)
        if turno:
            return jsonify({'message': 'Estado del turno actualizado exitosamente', 'turno': turno.serialize()}), 200
        else:
            return jsonify({'message': 'Turno no encontrado'}), 404
    except Exception as e:
        return jsonify({'message': f'Error al actualizar el estado del turno: {str(e)}'}), 500

# Endpoint para obtener todos los turnos activos
@turno_bp.route('/turnos/activos', methods=['GET'])
def get_all_active_turnos():
    try:
        turnos = Turno.get_all_active()
        return jsonify([turno.serialize() for turno in turnos]), 200
    except Exception as e:
        return jsonify({'message': f'Error al obtener los turnos activos: {str(e)}'}), 500

# Endpoint para obtener el historial de turnos inactivos para una fecha específica
@turno_bp.route('/turnos/reporte', methods=['GET'])
def get_historial_turnos():
    fecha_str = request.args.get('fecha')
    if not fecha_str:
        return jsonify({'message': 'Fecha es requerida'}), 400

    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
        turnos = Turno.get_historial_by_date(fecha)
        return jsonify([turno.serialize() for turno in turnos]), 200
    except Exception as e:
        return jsonify({'message': f'Error al obtener el historial de turnos: {str(e)}'}), 500