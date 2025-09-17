from app import db

class Product(db.Model):
    """Modelo de producto para la tienda deportiva."""
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    exclusivo = db.Column(db.Boolean, default=False)
    galeria = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Product {}>'.format(self.nombre)
