from src.models.drogueria import db

class Eps(db.Model):
    __tablename__ = 'eps'

    id_eps = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)

    def serialize(self):
        return {
            'id_eps': self.id_eps,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'tipo': self.tipo
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, nombre, codigo, tipo):
        eps = cls(nombre=nombre, codigo=codigo, tipo=tipo)
        db.session.add(eps)
        db.session.commit()
        return eps
