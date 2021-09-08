from flask import Blueprint, render_template, flash, redirect, url_for, request
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Вы успешно вошли в аккаунт!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль!', category='error')
        else:
            flash('Такого пользователя не существует!', category='error')
    return render_template("auth/login.html", user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Такая почта уже зарегистрирована", category='error')
        elif len(name) < 3:
            flash("Имя пользователя не должно быть короче 3 символов!", category='error')
        elif len(password1) < 4:
            flash("Пароль не должен быть короче 4 симолов!", category='error')
        elif password1 != password2:
            flash("Пароли не совпадают!", category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Аккаунт успешно зарегистрирован!", category='success')
            return redirect(url_for('auth.login'))
    return render_template("auth/sign_up.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
