from flask import Flask, request, jsonify
from src.models.birthrecord_model import db
from src.models.request_model import db
from src.routes.birthrecord_routes import birthrecord_route
from src.routes.request_routes import request_route
from src.services.birthrecord_service import save_birth_record
from PIL import Image
import pytesseract
import os
import re

# Especificar la ubicación del ejecutable de Tesseract OCR
pytesseract.tesseract_cmd = r'C:\Users\pc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

app = Flask(__name__, template_folder='src/view')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:victor8680544@localhost/db_python'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta para guardar los archivos subidos
db.init_app(app)


app.register_blueprint(birthrecord_route)
app.register_blueprint(request_route)

# Crear las tablas
with app.app_context():
    db.create_all()

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

            # Guardar datos en la base de datos
            success, error_message = save_birth_record(
                data["act_number"],
                data["full_name"],
                data["birth_date"],
                data["birth_time"],
                data["birth_place"]
            )

            if success:
                return jsonify({"message": "Datos extraídos y guardados exitosamente"}), 200
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
    # Find the act number
    match_acta = re.search(r'Acta N° (\d+)', text)
    act_number = match_acta.group(1) if match_acta else None

    # Find the names and surnames information
    match_names = re.search(r'nombre y apellidos: (.+?),', text, re.DOTALL)
    full_name = match_names.group(1) if match_names else None

    # Find the date of birth
    match_birth_date = re.search(r'nacio el dia (.+?)(?: del afios)? (.+?)\)', text)
    birth_date = match_birth_date.group(1) + ' ' + match_birth_date.group(2) if match_birth_date else None

    # Find the time of birth
    match_birth_time = re.search(r'a las (.+?) [APMapm.]+', text)
    birth_time = match_birth_time.group(1) if match_birth_time else None

    # Find the place of birth
    match_birth_place = re.search(r'en el (.+?)[APMapm.]+', text)
    birth_place = match_birth_place.group(1) if match_birth_place else None

    return {
        'act_number': act_number,
        'full_name': full_name,
        'birth_date': birth_date,
        'birth_time': birth_time,
        'birth_place': birth_place,
    }

if __name__ == '__main__':
    app.run(debug=True)
