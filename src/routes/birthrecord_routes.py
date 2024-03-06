from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_file
from src.services.request_service import RequestService
from src.services.birthrecord_service import BirthRecordService
from datetime import datetime, timedelta
import calendar
import qrcode
from fpdf import FPDF
import locale

birthrecord_route = Blueprint('birthrecord_route', __name__)

@birthrecord_route.route('/')
def index():
    return render_template('login.html')

@birthrecord_route.route('/register')
def register():
    return render_template('register.html')

@birthrecord_route.route('/extractdata')
def extract_data():
    return render_template('home.html')

@birthrecord_route.route('/generatebirthcertificate')
def generate_birthcertificate():
    all_requests = BirthRecordService.get_all_birth_records()
    all_requests2 = RequestService.get_all_requests()
    return render_template('generatebirthcertificate.html', all_requests=all_requests, all_requests2=all_requests2)

@birthrecord_route.route('/requesbirthcertificate')
def request_birthcertificate():
    all_requests = RequestService.get_all_requests()
    return render_template('requesbirthcertificate.html', all_requests=all_requests)

@birthrecord_route.route('/authwis')
def request_status():
    all_requests = RequestService.get_all_requests()
    all_requests1 = BirthRecordService.get_all_birth_records()
    return render_template('authwis.html', all_requests=all_requests, all_requests1=all_requests1)

@birthrecord_route.route('/createrequest',  methods=['GET', 'POST'])
def new_request():
    if request.method == 'POST':
        # Lógica para manejar el formulario y agregar el nuevo registro
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        status = "Pendiente"
        act_number = request.form.get('act_number')
        RequestService.create_request(act_number=act_number, name=name, last_name=lastname, status=status)

        return redirect(url_for('birthrecord_route.request_birthcertificate'))

    return render_template('requesbirthcertificate.html')


@birthrecord_route.route('/upload/<int:request_id>/<int:status>', methods=['GET'])
def updatereques(request_id,status):
    print(request_id)
    if status == 1:
        request_status = "Approved"
    else:
        request_status = "Rejected" 
    
    RequestService.update_request(request_id,request_status)
    
    return render_template('authwis.html')
    
    
    

@birthrecord_route.route('/generate_birth_certificate_pdf/<int:request_id>', methods=['GET'])
def generate_birth_certificate_pdf(request_id):
    request_info = BirthRecordService.get_birth_record_by_id(request_id)

    # Desempaqueta la tupla para acceder al diccionario
    request_dict, _ = request_info
    
    if request_info:
        # Crea el contenido del PDF utilizando la información de la solicitud
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.set_margins(20,20,20)

        pdf.cell(170,6, "República Bolivariana de Venezuela", ln=True, align='C')
        pdf.cell(150,6, "Consejo Nacional Electoral", ln=True, align='C')
        pdf.cell(150,6, "Comisión de Registro Civil Electoral", ln=True, align='C')
        pdf.cell(150,6, "Estado Bolívar  Municipio Caroni", ln=True, align='C')
        pdf.cell(150,6, "Registro Civil Municipal", ln=True, align='C')
        pdf.ln(4)
        pdf.cell(150,6, "ACTA DE NACIMIENTO", ln=True, align='C')
        pdf.ln(4)
        # Configurar la fuente y tamaño para el contenido
        pdf.set_font("Arial", size=10)

        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_actual = datetime.now()
        fecha_nueva = fecha_actual + timedelta(days=15)
        nombre_mes = calendar.month_name[fecha_nueva.month]
        
        fecha_formateada = f"{fecha_nueva.day} días del Mes de {nombre_mes} del Año {fecha_nueva.year}"

        acta_text = f"""Acta No {request_dict['record_number']} ... {request_dict['full_name']}\nLCDA, MAGVIS ELENA TOLEDO ROMERO, C.I: 14.044.797, Directora del Registro Civil Municipal designada por el Ciudadano TITO JOSE OVIEDO Alcalde y Primera Autoridad Civil del Municipio Caroni del Estado Bolivar, segun Resolucion No {request_dict['resolution_number']} de fecha {request_dict['date']}, hago constar que hoy {request_dict['written_date']}, me ha sido presentada ante este Despacho, un nino por: {request_dict['father_name']}; de {request_dict['father_age']} anos de edad, {request_dict['father_status']}, Titular de la Cedula de Identidad No  {request_dict['ci_father']}, Domiciliado en {request_dict['addres']}, quien manifesto que el nino cuya presentacion hace, nacio en el Hospital {request_dict['birth_hospital']} de {request_dict['hospital_place']}, Ubicado en {request_dict['location_place']}, el dia: {request_dict['day_birth']}; a las {request_dict['time_birth']} Horas; que tiene por Nombre: {request_dict['full_name']}; Quien es su hijo a quien Reconoce en este Acto Conforme a la Ley y de la Ciudadana: {request_dict['mather_name']}; de {request_dict['mather_age']} anos de edad, {request_dict['mather_status']}, Titular de la Cedula de Identidad No  {request_dict['ci_mather']}, Domiciliado en {request_dict['resided_mather']}. Acta levantada de Conformidad con la Resolucion No {request_dict['resolution']} de Fecha {request_dict['resolution_date']}, Publicada en Gaceta Oficial No {request_dict['gazette']} de fecha {request_dict['gazette_date']} Emitida por el Consejo Nacional Electoral. Se hace constar que esta Presentacion se realiza segun Constancia de Nacimiento No {request_dict['Birth_Certificate']} Expedida por el Hospital {request_dict['birth_hospital']} de {request_dict['hospital_place']}. Fueron Testigos Presenciales de este Acto: {request_dict['witnesses_birth']}, Titulares de las Cedulas de Identidad No: {request_dict['witnesses_ci']}, Respectivamente, venezolanos, Mayores de edad y Vecinos de esta Parroquia. La Presente Acta, quedo Registrada bajo el Numero {request_dict['record_number']}, Libro No {request_dict['number_book']}, del Ano {request_dict['year']}, de los Libros de Registro de Nacimientos Llevados por este Registro Civil. Se Leyo y Conformen Firman
                    """


        pdf.multi_cell(0, 6, txt=acta_text, align='J')  

        pdf.ln(4)
        pdf.cell(170,6, "DIRECTORA DEL REGISTRO CIVIL MUNICIPAL", ln=True, align='C')
        pdf.cell(170,6, "El Presentante", ln=True, align='J')
        pdf.ln(10)

        pdf.cell(170,6, "Los Testigos", ln=True, align='J')
        pdf.ln(10)

        expitarion = f"Es Copia Fiel y Exacta de su Original que se Expide a los {fecha_formateada}"
        pdf.multi_cell(0, 4, txt=expitarion, align='J')

        pdf.cell(150,6, "Valida con Firma y Sello Humedo", align='J')
        pdf.cell(150,6, "Válido por 15 dias", align='J')

        # Guarda el PDF en un archivo temporal
        pdf_path = f'uploads/pdf_file_{request_id}.pdf'
        pdf.output(pdf_path)

        # Devuelve el PDF como archivo para su descarga
        return send_file(pdf_path, as_attachment=True)
    else:
        return jsonify({"error": "Request not found"})



@birthrecord_route.route('/generate_qr/<int:request_id>', methods=['GET'])
def generate_qr(request_id):
    request_info = BirthRecordService.get_birth_record_by_id(request_id)
    request_dict, _ = request_info
    qr_content = f"Partida de naciemiento Nombre: {request_dict['record_number']}, Apellido: {request_dict['full_name']}"

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

        success, error_message = BirthRecordService.save_birth_record(record_number, names, birth_date, birth_time, place_birth)

        if success:
            return jsonify({"message": "Record saved successfully"}), 200
        else:
            return jsonify({"error": f"Error saving record: {error_message}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error in request: {str(e)}"}), 400


