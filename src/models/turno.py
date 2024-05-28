from src.models.drogueria import db

# Modelo para los turnos de la aplicación
class Turno(db.Model):
    __tablename__ = 'turnos'

    # Campos de la tabla "turnos"
    id_turno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_drogueria = db.Column(db.Integer, db.ForeignKey('droguerias.id_drogueria'), nullable=False)
    la_receta_medica = db.Column(db.Integer, db.ForeignKey('recetas_medicas.id_receta_medica'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, nullable=False)
    fecha_finalizacion = db.Column(db.DateTime, nullable=True)
    novedades = db.Column(db.Text, nullable=True)
    limite_recetas = db.Column(db.Integer, nullable=False)

    # Las relaciones que se tiene con otras tablas
    drogueria = db.relationship('Drogueria', backref=db.backref('turnos', lazy=True))
    receta_medica = db.relationship('RecetaMedica', backref=db.backref('turnos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('turnos', lazy=True))

    # Serializa el objeto Turno a un formato JSON-friendly
    def serialize(self):
        return {
            'id_turno': self.id_turno,
            'id_drogueria': self.id_drogueria,
            'la_receta_medica': self.la_receta_medica,
            'id_usuario': self.id_usuario,
            'estado': self.estado,
            'tipo': self.tipo,
            'fecha_asignacion': self.fecha_asignacion.isoformat(),
            'fecha_finalizacion': self.fecha_finalizacion.isoformat() if self.fecha_finalizacion else None,
            'novedades': self.novedades,
            'limite_recetas': self.limite_recetas
        }

    # Obtiene todos los turnos almacenados
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # Crea un nuevo turno con los parámetros establecidos y lo guarda en la base de datos
    @classmethod
    def create(cls, id_drogueria, la_receta_medica, id_usuario, estado, tipo, fecha_asignacion, fecha_finalizacion, novedades, limite_recetas):
        turno = cls(
            id_drogueria=id_drogueria, la_receta_medica=la_receta_medica, id_usuario=id_usuario,
            estado=estado, tipo=tipo, fecha_asignacion=fecha_asignacion,
            fecha_finalizacion=fecha_finalizacion, novedades=novedades, limite_recetas=limite_recetas
        )
        db.session.add(turno)
        db.session.commit()
        return turno

    # Obtiene el turno activo de un usuario específico
    @classmethod
    def get_active_turn_by_user(cls, id_usuario):
        return cls.query.filter_by(id_usuario=id_usuario, estado='Activo').first()

    # Obtiene todos los turnos activos
    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(estado='Activo').all()

    # Actualiza el estado de un turno especifico
    @classmethod
    def update_estado(cls, id_turno, nuevo_estado):
        turno = cls.query.get(id_turno)
        if turno:
            turno.estado = nuevo_estado
            db.session.commit()
            return turno
        return None

    # Obtiene el historial de turnos inactivos para una fecha específica
    @classmethod
    def get_historial_by_date(cls, fecha):
        return cls.query.filter(
            cls.estado == 'Inactivo',
            db.func.date(cls.fecha_finalizacion) == fecha
        ).all()