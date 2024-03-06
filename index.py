from flask import Flask, request, jsonify,redirect,url_for
from src.models.request_model import db
from src.models.users_model import User
from src.routes.birthrecord_routes import birthrecord_route
from src.routes.request_routes import request_route
from src.routes.user_routes import user_route
from src.services.birthrecord_service import BirthRecordService
from src.services.user_service import UserService
from PIL import Image
import pytesseract
import os
import spacy

# Cargar el modelo en español de spaCy
nlp = spacy.load("es_core_news_sm")

# Especificar la ubicación del ejecutable de Tesseract OCR
pytesseract.tesseract_cmd = r'C:\Users\pc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

app = Flask(__name__, template_folder='src/view')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:victor8680544@localhost/db_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  
db.init_app(app)

app.register_blueprint(birthrecord_route)
app.register_blueprint(request_route)
app.register_blueprint(user_route)

# Crear las tablas
with app.app_context():
    db.create_all()

@app.route('/auth', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = verify_password(email, password)
        
        if user:
            if user.rol == "user":
                return redirect(url_for('birthrecord_route.request_birthcertificate'))
            else:
                return redirect(url_for('birthrecord_route.extract_data'))
        else:    
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
        
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return user
    else:
        return False
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        rol = request.form.get('rol')
        
        UserService.create_user(email,password, rol)
        
        if rol == "user":
            return redirect(url_for('birthrecord_route.request_birthcertificate'))
        else:
            return redirect(url_for('birthrecord_route.extract_data'))
        
@app.route('/updatereques', methods=['POST'])

# Ruta para manejar la carga de archivos
@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No se proporcionó ningún archivo"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "Nombre de archivo vacío"}), 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Extraer text de la imagen
            extracted_text = extract_text_from_image(file_path)
            
            data = extract_info_from_text(extracted_text)

            print(data)

            success, error_message = BirthRecordService.save_birth_record(
                data["act_number"],
                data["full_name"],
                data["resolution_number"],
                data["date"],
                data["written_date"],
                data["father_name"],
                data["father_age"],
                data["father_status"],
                data["ci_father"],
                data["addres"],
                data["birth_hospital"],
                data["hospital_place"],
                data["location_place"],
                data["day_birth"],
                data["time_birth"],
                data["mather_name"],
                data["mather_age"],
                data["mather_status"],
                data["ci_mather"],
                data["resided_mather"],
                data["resolution"],
                data["resolution_date"],
                data["gazette"],
                data["gazette_date"],
                data["Birth_Certificate"],
                data["witnesses_birth"],
                data["witnesses_ci"],
                data["number_book"],
                data["year"]
            )

            if success:
                return redirect(url_for('birthrecord_route.request_status'))
            else:
                return jsonify({"error": f"Error al guardar en la base de datos: {error_message}"}), 500
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado"}), 400
    except Exception as e:
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 400

def extract_text_from_image(file_path):
    # Utilizar pytesseract para extraer text de la imagen
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

def extract_info_from_text(text):

    # Procesar el texto con spaCy
    doc = nlp(text)

    tokens = doc[35:36]
    act_number = ' '.join(token.text for token in tokens)
            
    tokens = doc[37:41]
    full_name = ' '.join(token.text for token in tokens)

    tokens = doc[85:86]
    resolution_number = ' '.join(token.text for token in tokens)

    tokens = doc[88:89]
    date = ' '.join(token.text for token in tokens)

    tokens = doc[95:105]
    full_date = ' '.join(token.text for token in tokens)
    full_date = full_date.replace('\n', '')

    tokenss = doc[119:123]
    father_name = ' '.join(tokenss.text for tokenss in tokenss)

    age = doc[125:126]
    father_age = ' '.join(age.text for age in age)

    status = doc[130:137]
    father_status = ' '.join(status.text for status in status)
    father_status = father_status.replace('\n', '')

    father_ci = doc[144]

    adrres = doc[149:159]
    father_addres = ' '.join(adrres.text for adrres in adrres)

    birth_hospital = doc[177]
    
    place = doc[179:180]
    hospital_place = ' '.join(place.text for place in place)

    location = doc[186:194]
    location_place = ' '.join(location.text for location in location)

    day = doc[198:206]
    day_birth = ' '.join(day.text for day in day)
    day_birth = day_birth.replace('\n', '')

    time = doc[209:212]
    time_birth = ' '.join(time.text for time in time)

    mather = doc[248:253]
    mather_name =' '.join(mather.text for mather in mather)
    mather_name = mather_name.replace('\n', '')

    mather_age = doc[255]

    status2= doc[260:268]
    mather_status = ' '.join(status2.text for status2 in status2)
    mather_status = mather_status.replace('\n', '')

    ci_mather = doc[276]

    resided= doc[279:285]
    resided_mather = ' '.join(resided.text for resided in resided)
    resided_mather = resided_mather.replace('\n', '')

    resolution = doc[295]

    resolution_date = doc[299]

    gazette = doc[307]

    gazette_date = doc[310]

    Birth_Certificate = doc[334]

    witnesses = doc[353:359]
    witnesses_birth = ' '.join(witnesses.text for witnesses in witnesses)
    witnesses_birth = witnesses_birth.replace('\n', '')

    ci2 = doc[369:373]
    witnesses_ci = ' '.join(ci2.text for ci2 in ci2)
    witnesses_ci = witnesses_ci.replace('\n', '')

    number_book = doc[402]

    year = doc[407]

    return {
        'act_number': act_number,
        'full_name': full_name,
        'resolution_number': resolution_number,
        'date': date,
        'written_date': full_date,
        'father_name': father_name,
        'father_age': father_age,
        'father_status': father_status,
        'ci_father': father_ci,
        'addres': father_addres,
        'birth_hospital': birth_hospital,
        'hospital_place': hospital_place,
        'location_place': location_place,
        'day_birth': day_birth,
        'time_birth': time_birth,
        'mather_name': mather_name,
        'mather_age': mather_age,
        'mather_status': mather_status,
        'ci_mather': ci_mather,
        'resided_mather': resided_mather,
        'resolution': resolution,
        'resolution_date': resolution_date,
        'gazette': gazette,
        'gazette_date': gazette_date,
        'Birth_Certificate': Birth_Certificate,
        'witnesses_birth': witnesses_birth,
        'witnesses_ci': witnesses_ci,
        'number_book': number_book,
        'year': year,
    }

if __name__ == '__main__':
    app.run(debug=True)
