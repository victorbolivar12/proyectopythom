from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BirthRecord(db.Model):
    __tablename__ = 'birth_records'  # Puedes personalizar el nombre de la tabla

    id = db.Column(db.Integer, primary_key=True)
    record_number = db.Column(db.String(255), nullable=False)
    names = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.String(255), nullable=False)
    birth_time = db.Column(db.String(255), nullable=False)
    place_birth = db.Column(db.String(255), nullable=False)


    def __init__(self, record_number, names, birth_date, birth_time, place_birth):
        self.record_number = record_number
        self.names = names
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.place_birth = place_birth


    def __repr__(self):
        return f"<BirthRecord {self.id}>"


