
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models.users import Users
from app import db
bp = Blueprint('admin', __name__)

@bp.route('/admin/agregar_producto', methods=['POST'])
@login_required
def agregar_producto():
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    # Aquí deberías guardar el producto en la base de datos. Ejemplo:
    # nombre = request.form.get('nombre')
    # descripcion = request.form.get('descripcion')
    # precio = request.form.get('precio')
    # imagen_url = request.form.get('imagen_url')
    # categoria = request.form.get('categoria')
    # nuevo_producto = Product(nombre=nombre, descripcion=descripcion, precio=precio, imagen_url=imagen_url, categoria=categoria)
    # db.session.add(nuevo_producto)
    # db.session.commit()
    flash('Producto agregado correctamente (simulado, falta guardar en BD).', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    users = Users.query.all()
    return render_template('admin_dashboard.html', users=users)

@bp.route('/admin/bloquear/<int:user_id>')
@login_required
def bloquear_usuario(user_id):
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
def aceptar_pedido(pedido_id):
    if current_user.role != 'admin':
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('auth.dashboard'))
    # Aquí iría la lógica para aceptar el pedido del proveedor
    flash('Pedido aceptado.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
