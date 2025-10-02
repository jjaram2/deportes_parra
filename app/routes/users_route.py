from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models.books import Books
from app.models.authors import Authors
from app import db

bp = Blueprint('user', __name__)

@bp.route('/')
def index():
    data = Books.query.all()
    return render_template('books/index.html', data=data)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        titulo = request.form['titleBook']
        author = request.form['authorBook']
        
        new_book = Books(titleBook=titulo, authorBook=author)
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for('book.index'))
    
    data = Authors.query.all()
    return render_template('books/add.html', data=data)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book = Books.query.get_or_404(id)

    if request.method == 'POST':
        book.titleBook = request.form['titleBook']
        book.authorBook = request.form['authorBook']
        db.session.commit()        
        return redirect(url_for('book.index'))

    return render_template('books/edit.html', book=book)

@bp.route('/delete/<int:id>')
def delete(id):
    book = Books.query.get_or_404(id)
    
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('Book.index'))
@bp_client.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        current_user.nameUser = request.form['nameUser']
        # El rol normalmente no se modifica por el usuario
        db.session.commit()
        flash('Datos actualizados correctamente.')
        return redirect(url_for('client.perfil'))
    return render_template('perfil.html')
