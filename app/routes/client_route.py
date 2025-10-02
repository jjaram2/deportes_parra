from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db

bp_client = Blueprint('client', __name__)

@bp_client.route('/user-dashboard')
@login_required
def user_dashboard():
    return render_template('user_dashboard.html')

@bp_client.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        current_user.nameUser = request.form['nameUser']
        current_user.lastNameUser = request.form['lastNameUser']
        current_user.emailUser = request.form['emailUser']
        current_user.phoneUser = request.form['phoneUser']
        current_user.addressUser = request.form['addressUser']
        current_user.birthdateUser = request.form['birthdateUser']
        db.session.commit()
        flash('Datos actualizados correctamente.')
        return redirect(url_for('client.perfil'))
    return render_template('perfil.html')

@bp_client.route('/mis-compras')
@login_required
def mis_compras():
    compras = []  # Reemplaza con tu modelo de compras si lo tienes
    return render_template('mis_compras.html', compras=compras)