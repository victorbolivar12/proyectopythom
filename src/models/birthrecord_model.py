from flask_sqlalchemy import SQLAlchemy
from src.models.request_model import db

#db = SQLAlchemy()

class BirthRecord(db.Model):
    __tablename__ = 'birth_records'  

    id = db.Column(db.Integer, primary_key=True)
    record_number = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    resolution_number = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    written_date = db.Column(db.String(255), nullable=False)
    father_name = db.Column(db.String(255), nullable=False)
    father_age = db.Column(db.String(255), nullable=False)
    father_status = db.Column(db.String(255), nullable=False)
    ci_father = db.Column(db.String(255), nullable=False)
    addres = db.Column(db.String(255), nullable=False)
    birth_hospital = db.Column(db.String(255), nullable=False)
    hospital_place = db.Column(db.String(255), nullable=False)
    location_place = db.Column(db.String(255), nullable=False)
    day_birth = db.Column(db.String(255), nullable=False)
    time_birth = db.Column(db.String(255), nullable=False)
    mather_name = db.Column(db.String(255), nullable=False)
    mather_age = db.Column(db.String(255), nullable=False)
    mather_status = db.Column(db.String(255), nullable=False)
    ci_mather = db.Column(db.String(255), nullable=False)
    resided_mather = db.Column(db.String(255), nullable=False)
    resolution = db.Column(db.String(255), nullable=False)
    resolution_date = db.Column(db.String(255), nullable=False)
    gazette = db.Column(db.String(255), nullable=False)
    gazette_date = db.Column(db.String(255), nullable=False)
    Birth_Certificate = db.Column(db.String(255), nullable=False)
    witnesses_birth = db.Column(db.String(255), nullable=False)
    witnesses_ci = db.Column(db.String(255), nullable=False)
    number_book = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)

    def __init__(self, record_number, full_name, resolution_number, date, written_date,
                 father_name, father_age, father_status, ci_father, addres,
                 birth_hospital, hospital_place, location_place, day_birth, time_birth,
                 mather_name, mather_age, mather_status, ci_mather, resided_mather,
                 resolution, resolution_date, gazette, gazette_date,
                 Birth_Certificate, witnesses_birth, witnesses_ci, number_book, year):
        self.record_number = record_number
        self.full_name = full_name
        self.resolution_number = resolution_number
        self.date = date
        self.written_date = written_date
        self.father_name = father_name
        self.father_age = father_age
        self.father_status = father_status
        self.ci_father = ci_father
        self.addres = addres
        self.birth_hospital = birth_hospital
        self.hospital_place = hospital_place
        self.location_place = location_place
        self.day_birth = day_birth
        self.time_birth = time_birth
        self.mather_name = mather_name
        self.mather_age = mather_age
        self.mather_status = mather_status
        self.ci_mather = ci_mather
        self.resided_mather = resided_mather
        self.resolution = resolution
        self.resolution_date = resolution_date
        self.gazette = gazette
        self.gazette_date = gazette_date
        self.Birth_Certificate = Birth_Certificate
        self.witnesses_birth = witnesses_birth
        self.witnesses_ci = witnesses_ci
        self.number_book = number_book
        self.year = year

    def __repr__(self):
        return f"<BirthRecord {self.id}>"
