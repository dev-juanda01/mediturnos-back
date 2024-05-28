from src.models.drogueria import db

# Modelo para los pacientes en la aplicación
class Paciente(db.Model):
    __tablename__ = 'pacientes'

    # Campos de la tabla "pacientes"
    id_paciente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(255), nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    tipo_documento = db.Column(db.String(50), nullable=False)
    eps = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(255), nullable=False)

    # Serializa el objeto Paciente en un diccionario JSON
    def serialize(self):
        return {
            'id_paciente': self.id_paciente,
            'nombre': self.nombre,
            'documento': self.documento,
            'tipo_documento': self.tipo_documento,
            'eps': self.eps,
            'telefono': self.telefono,
            'correo': self.correo
        }

    # Obtiene todos los pacientes almacenados en la base de datos
    @classmethod
    def get_all(cls):
        return cls.query.all()

    # Crea un nuevo paciente y lo guarda en la base de datos
    @classmethod
    def create(cls, nombre, documento, tipo_documento, eps, telefono, correo):
        paciente = cls(nombre=nombre, documento=documento, tipo_documento=tipo_documento, eps=eps, telefono=telefono, correo=correo)
        db.session.add(paciente)
        db.session.commit()
        return paciente