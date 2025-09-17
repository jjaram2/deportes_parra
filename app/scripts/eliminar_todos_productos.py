
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../../'))
from app import create_app, db
from app.models.products import Product

app = create_app()
with app.app_context():
    Product.query.delete()
    db.session.commit()
    print("Todos los productos han sido eliminados de la base de datos.")
