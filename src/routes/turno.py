from flask import Blueprint, request, jsonify
from src.models.turno import Turno, db
from datetime import datetime
import pytz
import pyodbc

turno_bp = Blueprint('turno_bp', __name__)

@turno_bp.route('/turnos', methods=['GET'])
def get_turnos():
    try:
        turnos = Turno.get_all()
        return jsonify([turno.serialize() for turno in turnos]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

    if not id_drogueria or not la_receta_medica or not id_usuario or not estado or not tipo or not fecha_asignacion_str or not limite_recetas:
        return jsonify({'message': 'Faltan datos'}), 400

    try:
        # Convertir fecha_asignacion_str y fecha_finalizacion_str a objetos datetime
        local_tz = pytz.timezone('America/Bogota')
        fecha_asignacion = local_tz.localize(datetime.strptime(fecha_asignacion_str, '%Y-%m-%d %H:%M:%S'))
        fecha_finalizacion = local_tz.localize(datetime.strptime(fecha_finalizacion_str, '%Y-%m-%d %H:%M:%S')) if fecha_finalizacion_str else None

        # Conexión a la base de datos utilizando pyodbc
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-IMIOCSF\\SQLEXPRESS;DATABASE=medi_turnos;Trusted_Connection=yes;')
        cursor = conn.cursor()

        # Ejecutar la inserción usando parámetros
        cursor.execute("""
            INSERT INTO turnos (id_drogueria, la_receta_medica, id_usuario, estado, tipo, fecha_asignacion, fecha_finalizacion, novedades, limite_recetas)
            OUTPUT inserted.id_turno
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_drogueria, la_receta_medica, id_usuario, estado, tipo, fecha_asignacion, fecha_finalizacion, novedades, limite_recetas))

        turno_id = cursor.fetchone()[0]  # Obtener el id del turno insertado

        conn.commit()  # Confirmar la transacción

        return jsonify({'message': 'Turno creado exitosamente', 'id_turno': turno_id}), 201
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()  # Revertir la transacción en caso de error
        return jsonify({'message': f'Error al crear turno: {str(e)}'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



