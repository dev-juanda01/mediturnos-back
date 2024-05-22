# from flask_sqlalchemy import SQLAlchemy
from src.models.drogueria import db
from config import Config
from flask import Flask

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'codigo': self.codigo,
            'correo': self.correo
        }

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, nombre, telefono, direccion, codigo, correo, password):
        usuario = cls(nombre=nombre, telefono=telefono, direccion=direccion, codigo=codigo, correo=correo, password=password)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @classmethod
    def login(cls, correo, password):
        return cls.query.filter_by(correo=correo, password=password).first()