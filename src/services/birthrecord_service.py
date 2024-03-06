from src.models.birthrecord_model import BirthRecord
from src.models.request_model import db

class BirthRecordService:
    @staticmethod
    def save_birth_record(record_number, full_name, resolution_number, date, written_date,
                          father_name, father_age, father_status, ci_father, addres,
                          birth_hospital, hospital_place, location_place, day_birth, time_birth,
                          mather_name, mather_age, mather_status, ci_mather, resided_mather,
                          resolution, resolution_date, gazette, gazette_date,
                          Birth_Certificate, witnesses_birth, witnesses_ci, number_book, year):
        new_record = BirthRecord(
            record_number=record_number,
            full_name=full_name,
            resolution_number=resolution_number,
            date=date,
            written_date=written_date,
            father_name=father_name,
            father_age=father_age,
            father_status=father_status,
            ci_father=ci_father,
            addres=addres,
            birth_hospital=birth_hospital,
            hospital_place=hospital_place,
            location_place=location_place,
            day_birth=day_birth,
            time_birth=time_birth,
            mather_name=mather_name,
            mather_age=mather_age,
            mather_status=mather_status,
            ci_mather=ci_mather,
            resided_mather=resided_mather,
            resolution=resolution,
            resolution_date=resolution_date,
            gazette=gazette,
            gazette_date=gazette_date,
            Birth_Certificate=Birth_Certificate,
            witnesses_birth=witnesses_birth,
            witnesses_ci=witnesses_ci,
            number_book=number_book,
            year=year
        )

        try:
            db.session.add(new_record)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)
        finally:
            db.session.close()

    @staticmethod
    def get_birth_record_by_id(record_id):
        try:
            record = BirthRecord.query.get(record_id)
            if record:
                return {
                    "id": record.id,
                    "record_number": record.record_number,
                    "full_name": record.full_name,
                    "resolution_number": record.resolution_number,
                    "date": record.date,
                    "written_date": record.written_date,
                    "father_name": record.father_name,
                    "father_age": record.father_age,
                    "father_status": record.father_status,
                    "ci_father": record.ci_father,
                    "addres": record.addres,
                    "birth_hospital": record.birth_hospital,
                    "hospital_place": record.hospital_place,
                    "location_place": record.location_place,
                    "day_birth": record.day_birth,
                    "time_birth": record.time_birth,
                    "mather_name": record.mather_name,
                    "mather_age": record.mather_age,
                    "mather_status": record.mather_status,
                    "ci_mather": record.ci_mather,
                    "resided_mather": record.resided_mather,
                    "resolution": record.resolution,
                    "resolution_date": record.resolution_date,
                    "gazette": record.gazette,
                    "gazette_date": record.gazette_date,
                    "Birth_Certificate": record.Birth_Certificate,
                    "witnesses_birth": record.witnesses_birth,
                    "witnesses_ci": record.witnesses_ci,
                    "number_book": record.number_book,
                    "year": record.year
                }, None
            else:
                return None, f"No se encontró ningún registro con el ID {record_id}"
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_all_birth_records():
        try:
            records = BirthRecord.query.all()
            result = []
            for record in records:
                result.append({
                    "id": record.id,
                    "record_number": record.record_number,
                    "full_name": record.full_name,
                    "resolution_number": record.resolution_number,
                    "date": record.date,
                    "written_date": record.written_date,
                    "father_name": record.father_name,
                    "father_age": record.father_age,
                    "father_status": record.father_status,
                    "ci_father": record.ci_father,
                    "addres": record.addres,
                    "birth_hospital": record.birth_hospital,
                    "hospital_place": record.hospital_place,
                    "location_place": record.location_place,
                    "day_birth": record.day_birth,
                    "time_birth": record.time_birth,
                    "mather_name": record.mather_name,
                    "mather_age": record.mather_age,
                    "mather_status": record.mather_status,
                    "ci_mather": record.ci_mather,
                    "resided_mather": record.resided_mather,
                    "resolution": record.resolution,
                    "resolution_date": record.resolution_date,
                    "gazette": record.gazette,
                    "gazette_date": record.gazette_date,
                    "Birth_Certificate": record.Birth_Certificate,
                    "witnesses_birth": record.witnesses_birth,
                    "witnesses_ci": record.witnesses_ci,
                    "number_book": record.number_book,
                    "year": record.year
                })
            return result
        except Exception as e:
            print(f"Error al obtener registros de nacimiento: {e}")
            return []
