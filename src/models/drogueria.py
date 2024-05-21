from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask

# app = Flask(__name__)
# app.config.from_object(Config)

# Inicializar SQLAlchemy
db = SQLAlchemy()

class Drogueria(db.Model):
    __tablename__ = 'droguerias'
    id_drogueria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id_drogueria': self.id_drogueria,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'codigo': self.codigo
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, nombre, direccion, codigo):
        drogueria = cls(nombre=nombre, direccion=direccion, codigo=codigo)
        db.session.add(drogueria)
        db.session.commit()
        return drogueria

