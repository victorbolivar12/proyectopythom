from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_file
from src.models.birthrecord_model import db
from src.services.request_service import RequestService
from src.services.birthrecord_service import save_birth_record
from datetime import datetime
import qrcode
from fpdf import FPDF

birthrecord_route = Blueprint('birthrecord_route', __name__)

@birthrecord_route.route('/')
def index():
    return render_template('home.html')

@birthrecord_route.route('/generatebirthcertificate')
def generate_birthcertificate():
    all_requests = RequestService.get_all_requests()
    return render_template('generatebirthcertificate.html', all_requests=all_requests)

@birthrecord_route.route('/requesbirthcertificate')
def request_birthcertificate():
    all_requests = RequestService.get_all_requests()
    return render_template('requesbirthcertificate.html', all_requests=all_requests)

@birthrecord_route.route('/createrequest',  methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        # Lógica para manejar el formulario y agregar el nuevo registro
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        status = request.form.get('status')
        duration = request.form.get('duration')
        RequestService.create_request(name=name, last_name=lastname, status=status, duration=duration)

        return redirect(url_for('birthrecord_route.request_birthcertificate'))

    return render_template('requesbirthcertificate.html')

@birthrecord_route.route('/generate_birth_certificate_pdf/<int:request_id>', methods=['GET'])
def generate_birth_certificate_pdf(request_id):
    request_info = RequestService.get_request_by_id(request_id)

    if request_info:
        # Crea el contenido del PDF utilizando la información de la solicitud
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_margins(30,30,30)

        # Agregar las líneas de texto al encabezado centrado
        header_lines = [
            "Republica Bolivariana de Venezuela",
            "Consejo Nacional Electoral",
            "Municipio Piar Estado Monagas",
            "Comisión de Registro Civil y Electoral",
            "Municipio Piar Estado Monagas"
        ]

        for line in header_lines:
            pdf.cell(150, 6, txt=line, ln=True, align='C')

        # Configurar la fuente y tamaño para el contenido
        pdf.set_font("Arial", size=10)

        # Agregar espacio después del encabezado centrado
        pdf.ln(10)

        # Agregar los nombres y apellidos al contenido del PDF
        content = f"""Quien suscribe, Abogada: ROSA VIRGINIA GOMEZ CHACON, Venezolana, mayor de edad, titular de la cedula de identidad Nº V-19.781.397 Registradora Civil del Municipio Piar Estado Monagas, Segun Resolucion Numero AMP-DA002-2014 de Fecha  Dieciseis de Enero de Dos Mil Catorce,(2014) y publicado en gaceta municipal extraordinaria Nº 002,  de fecha Diecisiete (17) de Enero de(2014), CERTIFICA: que la copia de Nacimiento que a continuacionse expresa es trasladada fiel y exacta de su original que dice asi Acta Nº 108. Folio 111. Tomo 1. TSU Miguel Ramon Fuentes Gil, Primera autoridad Civil del municipio Piar del estado Monagas. Hace constar que hoy doce de febrero del año dos mil diecisiete, me ha sido presentado en este despacho un niño varon por elciudadano: {request_info['name']} {request_info['last_name']}, de treinta y siete años de edad, venezolano, titular de la cedula de identidad Nº V-18.173.338, natural de la ciudad de Aragua de Maturin, municipio Piar del estado Monagas, y residenciado en la poblacion de Chaparral, municipio Piar del estado Monagas y expuso: Quepresenta a su hijo. CARLOS ADRIAN URBANEJA SIFONTES, nacido en el HospitalUniversitario Dr. Manuel Nunez Tovar, de la ciudad de Maturin, municipio Maturin,del estado Monagas el dia doce de enero del año dos mil diecisiete, hijo deMARIA CAROLINA SIFONTES de treinta y un años (31) de edad, venezolana, soltera de oficios del hogar, titular de la cedula de identidad Nº V-18.510.072,natural de la poblacion de Chaguaramal municipio Piar del estado Monagas yresidenciada al igual que el presentante. Fueron testigos presenciales de este actolos ciudadanos: Felipe Antonio Gomez Malave y Juan Carlos Espinoza Palomo,mayores de edad, venezolanos, titulares de las cedulas de identidad Nros:4.717.192 y 12.960.945, respectivamente y de este domicilio. Leida la presenteacta al presentante y testigos manifestaron su conformidad y firman. El Alcalde(fdo ilegible). El presentante (fdo) legible. Los testigos (fdos) ilegibles. Lasecretaria (fdo) ilegible. Hay sello del registro civil. Expido la presente a peticion dela parte interesada en Aragua de Maturin, a los catorce dias del mes de dos mil diecisiete."""

        pdf.multi_cell(0, 6, txt=content, align='L')  # Quité ln=True

        # Guarda el PDF en un archivo temporal
        pdf_path = f'uploads/pdf_file_{request_id}.pdf'
        pdf.output(pdf_path)

        # Devuelve el PDF como archivo para su descarga
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({"error": "Request not found"})



@birthrecord_route.route('/generate_qr/<int:request_id>', methods=['GET'])
def generate_qr(request_id):
    request_info = RequestService.get_request_by_id(request_id)
    qr_content = f"Partida de naciemiento Nombre: {request_info['name']}, Apellido: {request_info['last_name']}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guarda el código QR en un archivo temporal
    qr_path = f'uploads/qr_code_{request_id}.png'
    img.save(qr_path)

    # Devuelve el código QR como archivo para su descarga
    return send_file(qr_path, as_attachment=True)

@birthrecord_route.route('/save_record', methods=['POST'])
def save_record():
    try:
        data = request.get_json() 
        record_number = data['record_number']
        names = data['names']
        birth_date = data['birth_date']
        birth_time = data['birth_time']
        place_birth = data['place_birth']

        success, error_message = save_birth_record(record_number, names, birth_date, birth_time, place_birth)

        if success:
            return jsonify({"message": "Record saved successfully"}), 200
        else:
            return jsonify({"error": f"Error saving record: {error_message}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error in request: {str(e)}"}), 400


