from src.models.drogueria import db

class Medicamento(db.Model):
    __tablename__ = 'medicamentos'
    id_medicamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    laboratorio = db.Column(db.String(255), nullable=False)
    dosis_medica = db.Column(db.String(255), nullable=False)
    concentracion = db.Column(db.String(255), nullable=False)
    presentacion = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id_medicamento': self.id_medicamento,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'stock': self.stock,
            'laboratorio': self.laboratorio,
            'dosis_medica': self.dosis_medica,
            'concentracion': self.concentracion,
            'presentacion': self.presentacion,
            'tipo': self.tipo
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, nombre, codigo, stock, laboratorio, dosis_medica, concentracion, presentacion, tipo):
        medicamento = cls(
            nombre=nombre, codigo=codigo, stock=stock, laboratorio=laboratorio,
            dosis_medica=dosis_medica, concentracion=concentracion,
            presentacion=presentacion, tipo=tipo
        )
        db.session.add(medicamento)
        db.session.commit()
        return medicamento
