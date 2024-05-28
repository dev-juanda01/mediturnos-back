from src.models.drogueria import db

class Turno(db.Model):
    __tablename__ = 'turnos'

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

    drogueria = db.relationship('Drogueria', backref=db.backref('turnos', lazy=True))
    receta_medica = db.relationship('RecetaMedica', backref=db.backref('turnos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('turnos', lazy=True))

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

    @classmethod
    def get_all(cls):
        return cls.query.all()

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
    @classmethod
    def get_active_turn_by_user(cls, id_usuario):
        return cls.query.filter_by(id_usuario=id_usuario, estado='Activo').first()

    @classmethod
    def update_estado(cls, id_turno, nuevo_estado):
        turno = cls.query.get(id_turno)
        if turno:
            turno.estado = nuevo_estado
            db.session.commit()
            return turno
        return None