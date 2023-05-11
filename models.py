from app import db
# Definimos nuestro modelo de datos
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f'id {self.id}:,' \
               f'Nombre: {self.nombre},' \
               f'Apellido: {self.apellido},' \
               f'Email: {self.email}'

    def __repr__(self):
        return f'<Persona: {self.nombre} {self.apellido}>'

