from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask

# app = Flask(__name__)
# app.config.from_object(Config)

# Inicializar SQLAlchemy
db = SQLAlchemy()

# Modelo para la tabla 'droguerias'
class Drogueria(db.Model):
    __tablename__ = 'droguerias'

    # Campos de la tabla "droguerias"
    id_drogueria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)

    # Serializa el objeto drogueria a un formato JSON
    def serialize(self):
        return {
            'id_drogueria': self.id_drogueria,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'codigo': self.codigo
        }

    # Retorna todas las droguerías almacenadas
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # Crea una nueva entrada de droguería
    @classmethod
    def create(cls, nombre, direccion, codigo):
        drogueria = cls(nombre=nombre, direccion=direccion, codigo=codigo)
        db.session.add(drogueria)
        db.session.commit()
        return drogueria