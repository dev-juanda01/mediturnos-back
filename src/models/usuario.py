# from flask_sqlalchemy import SQLAlchemy
from src.models.drogueria import db
from config import Config
from flask import Flask

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)

# Modelo para los usuarios en la aplicación
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    # Campos de la tabla 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    codigo = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # Serializa el objeto Usuario a un formato JSON-friendly
    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'codigo': self.codigo,
            'correo': self.correo
        }

    # Obtiene todos los usuarios almacenados
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # Crea un nuevo usuario con los parámetros dados y lo guarda en la base de datos
    @classmethod
    def create(cls, nombre, telefono, direccion, codigo, correo, password):
        usuario = cls(nombre=nombre, telefono=telefono, direccion=direccion, codigo=codigo, correo=correo, password=password)
        db.session.add(usuario)
        db.session.commit()
        return usuario

    # Verifica las credenciales de inicio de sesión de un usuario
    @classmethod
    def login(cls, correo, password):
        return cls.query.filter_by(correo=correo, password=password).first()