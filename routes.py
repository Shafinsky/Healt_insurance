from utils import is_admin
from models import Client, Policy, Claim, User
from forms import ClientForm, PolicyForm, ClaimForm
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, flash, request
from extensions import db
from flask_mail import Message
from extensions import mail

main_bp = Blueprint("main", __name__)


# ====================== HOME ======================
@main_bp.route("/")
def index():
    return render_template("index.html", title="Health Insurance System")


# ====================== CLIENTS ======================
@main_bp.route("/clients")
@main_bp.route("/clients/")
def clients_list():
    clients = Client.query.all()
    return render_template("clients/list.html", clients=clients)


@main_bp.route("/clients/create", methods=["GET", "POST"])
@main_bp.route("/clients/create/", methods=["GET", "POST"])
@login_required
def client_create():
    if not is_admin():
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.index"))

    form = ClientForm()

    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            owner_id=current_user.id
        )
        db.session.add(client)
        db.session.commit()
        flash("Клієнта успішно створено!", "success")
        return redirect(url_for("main.clients_list"))

    return render_template("clients/form.html", form=form)


@main_bp.route("/clients/<int:id>/edit", methods=["GET", "POST"])
@main_bp.route("/clients/<int:id>/edit/", methods=["GET", "POST"])
@login_required
def client_edit(id):
    if not is_admin():
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.index"))

    client = Client.query.get_or_404(id)
    form = ClientForm(obj=client)

    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash("Клієнта оновлено!", "success")
        return redirect(url_for("main.clients_list"))

    return render_template("clients/form.html", form=form)


@main_bp.route("/clients/<int:id>/delete")
@login_required
def client_delete(id):
    if not is_admin():
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.index"))

    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash("Клієнта видалено", "success")
    return redirect(url_for("main.clients_list"))


# ====================== POLICIES ======================
@main_bp.route("/policies")
@main_bp.route("/policies/")
def policies_list():
    policies = Policy.query.all()
    return render_template("policies/list.html", policies=policies)


@main_bp.route("/policies/create", methods=["GET", "POST"])
@main_bp.route("/policies/create/", methods=["GET", "POST"])
@login_required
def policy_create():
    form = PolicyForm()

    if form.validate_on_submit():
        policy = Policy(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            owner_id=current_user.id
        )
        db.session.add(policy)
        db.session.commit()
        flash("Поліс успішно створено!", "success")
        return redirect(url_for("main.policies_list"))

    return render_template("policies/form.html", form=form)


@main_bp.route("/policies/<int:id>/edit", methods=["GET", "POST"])
@main_bp.route("/policies/<int:id>/edit/", methods=["GET", "POST"])
@login_required
def policy_edit(id):
    policy = Policy.query.get_or_404(id)

    if not is_admin() and policy.owner_id != current_user.id:
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.policies_list"))

    form = PolicyForm(obj=policy)

    if form.validate_on_submit():
        form.populate_obj(policy)
        db.session.commit()
        flash("Поліс оновлено!", "success")
        return redirect(url_for("main.policies_list"))

    return render_template("policies/form.html", form=form)


@main_bp.route("/policies/<int:id>/delete")
@login_required
def policy_delete(id):
    policy = Policy.query.get_or_404(id)

    if not is_admin() and policy.owner_id != current_user.id:
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.policies_list"))

    db.session.delete(policy)
    db.session.commit()
    flash("Поліс видалено", "success")
    return redirect(url_for("main.policies_list"))


# ====================== CLAIMS ======================
@main_bp.route("/claims")
@main_bp.route("/claims/")
def claims_list():
    claims = Claim.query.all()
    return render_template("claims/list.html", claims=claims)


@main_bp.route("/claims/create", methods=["GET", "POST"])
@main_bp.route("/claims/create/", methods=["GET", "POST"])
@login_required
def claim_create():
    form = ClaimForm()

    if form.validate_on_submit():
        claim = Claim(
            description=form.description.data,
            owner_id=current_user.id,
            user_id=current_user.id,      # хто подав претензію
            status="Pending"
        )
        db.session.add(claim)
        db.session.commit()
        flash("Претензію подано!", "success")
        return redirect(url_for("main.claims_list"))

    return render_template("claims/form.html", form=form)


@main_bp.route("/claims/<int:id>/edit", methods=["GET", "POST"])
@main_bp.route("/claims/<int:id>/edit/", methods=["GET", "POST"])
@login_required
def claim_edit(id):
    claim = Claim.query.get_or_404(id)

    if not is_admin() and claim.owner_id != current_user.id:
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.claims_list"))

    form = ClaimForm(obj=claim)

    if form.validate_on_submit():
        form.populate_obj(claim)
        db.session.commit()
        flash("Претензію оновлено!", "success")
        return redirect(url_for("main.claims_list"))

    return render_template("claims/form.html", form=form)


@main_bp.route("/claims/<int:id>/delete")
@login_required
def claim_delete(id):
    claim = Claim.query.get_or_404(id)

    if not is_admin() and claim.owner_id != current_user.id:
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.claims_list"))

    db.session.delete(claim)
    db.session.commit()
    flash("Претензію видалено", "success")
    return redirect(url_for("main.claims_list"))


# ====================== APPROVE / REJECT ======================
@main_bp.route("/claims/<int:id>/approve")
@login_required
def approve_claim(id):

    if current_user.role != "admin":
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.claims_list"))

    claim = Claim.query.get_or_404(id)

    claim.status = "Approved"

    db.session.commit()

    user = User.query.get(claim.user_id)

    msg = Message(
        subject="Claim Approved",
        recipients=[user.email]
    )

    msg.body = f"""
    Hello {user.username}!

    Your claim #{claim.id} was approved successfully.
    """

    mail.send(msg)

    flash("Претензію схвалено", "success")

    return redirect(url_for("main.claims_list"))


@main_bp.route("/claims/<int:id>/reject")
@login_required
def reject_claim(id):
    if current_user.role != "admin":
        flash("Доступ заборонено", "danger")
        return redirect(url_for("main.claims_list"))

    claim = Claim.query.get_or_404(id)
    claim.status = "Rejected"
    db.session.commit()
    flash("Претензію відхилено", "danger")
    return redirect(url_for("main.claims_list"))

@main_bp.route("/admin")
@login_required
def admin_panel():

    if current_user.role != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("main.index"))

    users = User.query.all()

    return render_template(
        "admin/panel.html",
        users=users
    )

@main_bp.route("/admin/make-admin/<int:id>")
@login_required
def make_admin(id):

    if current_user.role != "admin":
        return redirect("/")

    user = User.query.get_or_404(id)

    user.role = "admin"

    db.session.commit()

    flash("User is now admin", "success")

    return redirect("/admin")

@main_bp.route("/admin/delete-user/<int:id>")
@login_required
def delete_user(id):

    if current_user.role != "admin":
        return redirect("/")

    user = User.query.get_or_404(id)

    db.session.delete(user)

    db.session.commit()

    flash("User deleted", "info")

    return redirect("/admin")
