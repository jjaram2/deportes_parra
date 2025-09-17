

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.users import Users
from app.models.products import Product
from app import db
bp = Blueprint('admin', __name__)

@bp.route('/admin/toggle_exclusivo/<int:producto_id>', methods=['POST'])
@login_required
def toggle_exclusivo(producto_id):
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    producto = Product.query.get_or_404(producto_id)
    producto.exclusivo = not producto.exclusivo
    try:
        db.session.commit()
        flash('Estado de exclusivo actualizado.', 'success')
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error al actualizar: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/toggle_galeria/<int:producto_id>', methods=['POST'])
@login_required
def toggle_galeria(producto_id):
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    producto = Product.query.get_or_404(producto_id)
    producto.galeria = not producto.galeria
    try:
        db.session.commit()
        flash('Estado de galería deportiva actualizado.', 'success')
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error al actualizar: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/eliminar_producto/<int:producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    """Elimina un producto si el usuario es admin."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    producto = Product.query.get_or_404(producto_id)
    try:
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado correctamente.', 'success')
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error al eliminar producto: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    """Edita un producto si el usuario es admin."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    producto = Product.query.get_or_404(producto_id)
    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.precio = int(request.form.get('precio'))
        producto.imagen_url = request.form.get('imagen_url')
        producto.categoria = request.form.get('categoria')
        try:
            db.session.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except db.exc.SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error al actualizar producto: {e}', 'danger')
    return render_template('editar_producto.html', producto=producto)

@bp.route('/admin/agregar_producto', methods=['POST'])
@login_required
def agregar_producto():
    """Agrega un producto si el usuario es admin."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    imagen_url = request.form.get('imagen_url')
    categoria = request.form.get('categoria').lower() if request.form.get('categoria') else None
    imagen_file = request.files.get('imagen_file')
    # Procesar imagen subida si no hay URL
    if not imagen_url and imagen_file and imagen_file.filename:
        import os
        from werkzeug.utils import secure_filename
        filename = secure_filename(imagen_file.filename)
        ruta_destino = os.path.join('app', 'static', 'img', 'productos', filename)
        imagen_file.save(ruta_destino)
        imagen_url = f'/static/img/productos/{filename}'
    if not (nombre and descripcion and precio and imagen_url and categoria):
        flash('Todos los campos son obligatorios.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    try:
        nuevo_producto = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio=int(precio),
            imagen_url=imagen_url,
            categoria=categoria
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto agregado correctamente.', 'success')
    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        flash(f'Error al agregar producto: {e}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin')
@login_required
def admin_dashboard():
    """Panel principal del administrador."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    users = Users.query.all()
    productos = Product.query.all()
    return render_template('admin_dashboard.html', users=users, productos=productos)

@bp.route('/admin/bloquear/<int:user_id>')
@login_required
def bloquear_usuario(user_id):
    """Bloquea un usuario cambiando su rol a 'bloqueado'."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    user = Users.query.get_or_404(user_id)
    user.role = 'bloqueado'
    db.session.commit()
    flash('Usuario bloqueado.', 'info')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/cambiar_rol/<int:user_id>', methods=['POST'])
@login_required
def cambiar_rol(user_id):
    """Cambia el rol de un usuario si el usuario es admin."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    user = Users.query.get_or_404(user_id)
    nuevo_rol = request.form.get('nuevo_rol')
    if nuevo_rol in ['admin', 'vendedor', 'usuario', 'proveedor']:
        user.role = nuevo_rol
        db.session.commit()
        flash('Rol actualizado.', 'success')
    else:
        flash('Rol inválido.', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin/aceptar_pedido/<int:pedido_id>')
@login_required
def aceptar_pedido(_):
    """Acepta el pedido de un proveedor (placeholder)."""
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    # Aquí iría la lógica para aceptar el pedido del proveedor
    flash('Pedido aceptado.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
