from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, mail
from models import User
from forms import RegisterForm, LoginForm   # LoginForm теж можна зробити
from flask_mail import Message

auth_bp = Blueprint("auth", __name__)


# ====================== REGISTER ======================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )

        db.session.add(user)
        db.session.commit()

        # EMAIL
        msg = Message(
            subject="Registration Successful",
            recipients=[user.email]
        )

        msg.body = f"""
        Hello {user.username}!

        Your account was created successfully.
        Welcome to Health Insurance System.
        """

        mail.send(msg)

        flash(
            "Акаунт успішно створено! Тепер ви можете увійти.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


# ====================== LOGIN ======================
@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            flash("Успішний вхід!", "success")
            return redirect(url_for("main.index"))

        else:
            flash("Невірний email або пароль", "danger")

    return render_template("login.html", form=form)


# ====================== LOGOUT ======================
@auth_bp.route("/logout")
@auth_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("Ви вийшли з системи", "info")
    return redirect(url_for("main.index"))