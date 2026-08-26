from extensions import db
from flask_login import UserMixin

policy_client = db.Table('policy_client',
    db.Column('policy_id', db.Integer, db.ForeignKey('policy.id'), primary_key=True),
    db.Column('client_id', db.Integer, db.ForeignKey('client.id'), primary_key=True))

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default="user")

    # Relationships
    client_profile = db.relationship(
        "Client",
        back_populates="user",
        uselist=False,
        foreign_keys="Client.user_id"
    )

    policies = db.relationship(
        "Policy",
        back_populates="owner",
        foreign_keys="Policy.owner_id"
    )

    claims = db.relationship(
        "Claim",
        back_populates="author",
        foreign_keys="Claim.user_id"
    )


class Client(db.Model):
    __tablename__ = 'client'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100))
    email = db.Column(db.String(120))

    # Two possible links to User - we must be explicit
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # Relationships
    owner = db.relationship(
        "User",
        foreign_keys=[owner_id],
        backref="owned_clients"   # optional
    )

    user = db.relationship(
        "User",
        back_populates="client_profile",
        foreign_keys=[user_id]
    )

    policies = db.relationship('Policy', secondary=policy_client, back_populates='clients')

    claims = db.relationship("Claim", back_populates="client")


class Policy(db.Model):
    __tablename__ = 'policy'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    duration = db.Column(db.Integer)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    owner = db.relationship(
        "User",
        back_populates="policies",
        foreign_keys=[owner_id]
    )

    claims = db.relationship("Claim", back_populates="policy")

    clients = db.relationship('Client', secondary=policy_client, back_populates='policies')



class Claim(db.Model):
    __tablename__ = 'claim'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="Pending")

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    policy_id = db.Column(db.Integer, db.ForeignKey("policy.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))   # who created the claim

    client = db.relationship("Client", back_populates="claims")
    policy = db.relationship("Policy", back_populates="claims")

    owner = db.relationship("User", foreign_keys=[owner_id])
    author = db.relationship(
        "User",
        back_populates="claims",
        foreign_keys=[user_id]
    )