from src.models.request_model import db 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password, rol):
        self.email = email
        self.password = password
        self.rol = rol

    def __repr__(self):
        return f"<User {self.id}>"
