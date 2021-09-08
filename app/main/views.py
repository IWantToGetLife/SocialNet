from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User
from app import db
from flask_login import current_user, login_required
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("index.html", user=current_user)


@views.route('/users')
@login_required
def users():
    user_list = User.query.order_by(User.id.asc()).all()
    return render_template("users.html", users=user_list, user=current_user)


@views.route('/users/<int:id>/delete')
@login_required
def user_delete(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    except:
        flash('Невозможно удалить пользователя!', category='error')
        return redirect('/users')


@views.route('/user/<name>')
@login_required
def user_profile(name):
    username = User.query.filter_by(name=name).first_or_404()
    return render_template('user.html', user=username)


@views.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    if request.method == 'POST':
        about_me = request.form.get('about')
        current_user.about_me = about_me
        db.session.commit()
        flash('Статус успешно обновлён!', category='success')
        return redirect(url_for('views.user_profile', name=current_user.name))
    return render_template('edit_profile.html', user=current_user)


@views.before_request
def before_req():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()
        db.session.commit()
