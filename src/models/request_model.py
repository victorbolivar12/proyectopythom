from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    act_number = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False)
    

    def __init__(self, act_number,name, last_name, status):
        self.act_number = act_number
        self.name = name
        self.last_name = last_name
        self.status = status

    def __repr__(self):
        return f"<Request {self.id}>"

