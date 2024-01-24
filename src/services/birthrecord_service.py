from src.models.birthrecord_model import db, BirthRecord

def save_birth_record(record_number, names, birth_date, birth_time, place_birth):
    new_record = BirthRecord(
        record_number=record_number,
        names=names,
        birth_date=birth_date,
        birth_time=birth_time,
        place_birth=place_birth
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
