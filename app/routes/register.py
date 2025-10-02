from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from app.models.users import Users
from werkzeug.security import generate_password_hash
import datetime

bp = Blueprint('register', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nameUser = request.form['nameUser']
        lastNameUser = request.form['lastNameUser']
        emailUser = request.form['emailUser']
        passwordUser = request.form['passwordUser']
        phoneUser = request.form.get('phoneUser')
        addressUser = request.form.get('addressUser')
        birthdateUser = request.form.get('birthdateUser')
        role = request.form.get('role', 'user')

        # Convertir la fecha a objeto date si existe
        birthdate_obj = None
        if birthdateUser:
            try:
                birthdate_obj = datetime.datetime.strptime(birthdateUser, "%Y-%m-%d").date()
            except ValueError:
                flash('Fecha de nacimiento inválida.', 'danger')
                return redirect(url_for('register.register'))

        if Users.query.filter_by(emailUser=emailUser).first():
            flash('El email ya está registrado.', 'danger')
            return redirect(url_for('register.register'))

        hashed_password = generate_password_hash(passwordUser)
        new_user = Users(
            nameUser=nameUser,
            lastNameUser=lastNameUser,
            emailUser=emailUser,
            passwordUser=hashed_password,
            phoneUser=phoneUser,
            addressUser=addressUser,
            birthdateUser=birthdate_obj,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')