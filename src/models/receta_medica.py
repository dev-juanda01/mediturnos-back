from src.models.drogueria import db

class RecetaMedica(db.Model):
    __tablename__ = 'recetas_medicas'

    id_receta_medica = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_eps = db.Column(db.Integer, nullable=False)
    medico = db.Column(db.String(255), nullable=False)
    id_medicamento = db.Column(db.Integer, db.ForeignKey('medicamentos.id_medicamento'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    codigo = db.Column(db.String(50), nullable=False)

    paciente = db.relationship('Paciente', backref=db.backref('recetas', lazy=True))
    medicamento = db.relationship('Medicamento', backref=db.backref('recetas', lazy=True))

    def serialize(self):
        return {
            'id_receta_medica': self.id_receta_medica,
            'id_paciente': self.id_paciente,
            'id_eps': self.id_eps,
            'medico': self.medico,
            'id_medicamento': self.id_medicamento,
            'fecha': self.fecha.isoformat(),
            'codigo': self.codigo
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, id_paciente, id_eps, medico, id_medicamento, fecha, codigo):
        receta = cls(
            id_paciente=id_paciente, id_eps=id_eps, medico=medico,
            id_medicamento=id_medicamento, fecha=fecha, codigo=codigo
        )
        db.session.add(receta)
        db.session.commit()
        return receta
