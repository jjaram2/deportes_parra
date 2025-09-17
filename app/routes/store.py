


"""
Rutas principales de la tienda deportiva: categorías, productos, carrito y checkout.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import current_user
from datetime import datetime
import random

bp = Blueprint('store', __name__)


@bp.route('/carrito/actualizar', methods=['POST'], endpoint='actualizar_carrito')
def store_actualizar_carrito():
    """Actualiza las cantidades de productos en el carrito."""
    cart = session.get('carrito', [])
    for item in cart:
        str_id = str(item['id'])
        nueva_cant = request.form.get(f'cantidades[{str_id}]')
        if nueva_cant:
            try:
                item['cantidad'] = max(1, int(nueva_cant))
            except ValueError:
                flash(f"Cantidad inválida para producto {item['nombre']}", 'danger')
    session['carrito'] = cart
    flash('Cantidades actualizadas', 'success')
    return redirect(url_for('store.carrito'))

@bp.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    """Procesa el pago y muestra la factura."""
    if not getattr(current_user, 'is_authenticated', False):
        flash('Debes iniciar sesión para realizar la compra.', 'warning')
        return redirect(url_for('auth.login'))
    carrito_factura = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito_factura) if carrito_factura else 0
    fecha = datetime.now().strftime('%d/%m/%Y %H:%M')
    numero = random.randint(100000, 999999)
    lugar = 'Tienda Deportiva Online'
    cliente = getattr(current_user, 'nombre', 'Cliente')
    session['carrito'] = []
    return render_template('factura.html', carrito=carrito_factura, total=total, fecha=fecha, numero=numero, lugar=lugar, cliente=cliente)

@bp.route('/carrito/vaciar', endpoint='vaciar_carrito')
def store_vaciar_carrito():
    """Vacía el carrito de compras."""
    session['carrito'] = []
    flash('Carrito vaciado', 'info')
    return redirect(url_for('store.carrito'))

@bp.route('/checkout', endpoint='checkout')
def store_checkout():
    """Muestra la página de checkout."""
    cart = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in cart) if cart else 0
    if not cart:
        flash('El carrito está vacío', 'warning')
        return redirect(url_for('store.carrito'))
    return render_template('checkout.html', carrito=cart, total=total)

@bp.route('/')
@bp.route('/home')
def home():
    """Página principal, redirige según el rol del usuario."""
    if getattr(current_user, 'is_authenticated', False):
        if getattr(current_user, 'role', None) == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif getattr(current_user, 'role', None) in ['vendedor', 'proveedor']:
            return redirect(url_for('auth.dashboard'))
        else:
            return redirect(url_for('auth.dashboard'))
    from app.models.products import Product
    productos = Product.query.all()
    return render_template('home.html', productos=productos)

@bp.route('/categorias')
def categorias():
    """Muestra las categorías deportivas."""
    categorias_list = [
        {
            'nombre': 'Fútbol',
            'url': '/categoria/futbol',
            'imagen': '/static/img/categorias/futbol.jpg',
            'descripcion': 'Balones, guayos, camisetas y accesorios para fútbol profesional y amateur.'
        },
        {
            'nombre': 'Baloncesto',
            'url': '/categoria/baloncesto',
            'imagen': '/static/img/categorias/baloncesto.jpg',
            'descripcion': 'Balones, zapatillas, tableros y ropa oficial para baloncesto de alto nivel.'
        },
        {
            'nombre': 'Tenis',
            'url': '/categoria/tenis',
            'imagen': '/static/img/categorias/tenis.jpg',
            'descripcion': 'Raquetas, pelotas, ropa y accesorios para jugadores de tenis.'
        },
        {
            'nombre': 'Natación',
            'url': '/categoria/natacion',
            'imagen': '/static/img/categorias/natacion.jpg',
            'descripcion': 'Gafas, trajes, gorros y accesorios para natación profesional y recreativa.'
        },
        {
            'nombre': 'Ciclismo',
            'url': '/categoria/ciclismo',
            'imagen': '/static/img/categorias/ciclismo.jpg',
            'descripcion': 'Bicicletas, cascos, uniformes y accesorios para ciclistas de todos los niveles.'
        },
        {
            'nombre': 'Camping',
            'url': '/categoria/camping',
            'imagen': '/static/img/categorias/camping.jpg',
            'descripcion': 'Carpas, mochilas, linternas y todo lo necesario para tus aventuras al aire libre.'
        },
        {
            'nombre': 'Fitness',
            'url': '/categoria/fitness',
            'imagen': '/static/img/categorias/fitness.jpg',
            'descripcion': 'Mancuernas, bandas, mats y equipos para entrenamiento físico y funcional.'
        },
        {
            'nombre': 'Accesorios',
            'url': '/categoria/accesorios',
            'imagen': '/static/img/categorias/accesorios.jpg',
            'descripcion': 'Botellas, bolsos, toallas y gadgets para complementar tu deporte favorito.'
        }
    ]
    return render_template('categorias.html', categorias=categorias_list)

@bp.route('/categoria/<string:nombre>')
def categoria(nombre):
    """Muestra los productos de una categoría (solo base de datos)."""
    from app.models.products import Product
    productos = Product.query.filter_by(categoria=nombre.lower()).all()
    return render_template('categorias.html', productos=productos, categoria=nombre)

@bp.route('/producto/<int:producto_id>')
def producto(producto_id):
    """Muestra el detalle de un producto."""
    from app.models.products import Product
    prod_db = Product.query.get(producto_id)
    if prod_db:
        relacionados = Product.query.filter_by(categoria=prod_db.categoria).filter(Product.id != producto_id).limit(4).all()
        return render_template('producto.html', producto=prod_db, relacionados=relacionados)
    else:
        return render_template('producto.html', producto=None, relacionados=[])

@bp.route('/carrito')
def carrito():
    """Muestra el carrito de compras."""
    cart = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in cart) if cart else 0
    return render_template('carrito.html', carrito=cart, total=total)

@bp.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
def agregar_carrito(producto_id):
    """Agrega un producto al carrito."""
    from app.models.products import Product
    prod = Product.query.get(producto_id)
    if not prod:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('store.carrito'))
    cantidad = int(request.form.get('cantidad', 1))
    item = {
        'id': prod.id,
        'nombre': prod.nombre,
        'precio': prod.precio,
        'cantidad': cantidad,
        'imagen_url': prod.imagen_url
    }
    cart = session.get('carrito', [])
    for p in cart:
        if p['id'] == item['id']:
            p['cantidad'] += cantidad
            break
    else:
        cart.append(item)
    session['carrito'] = cart
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('store.carrito'))

