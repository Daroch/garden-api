import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import User, Plant, AlertType, Alert
from schemas import AlertCreate
from sqlalchemy import select


EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
# print(EMAIL_USERNAME)


def send_email(email, subject, message_body):
    # Configurar los detalles del correo electrónico
    sender = EMAIL_USERNAME
    password = EMAIL_PASSWORD
    receiver = email

    # Crear el objeto del mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = sender
    mensaje['To'] = receiver
    mensaje['Subject'] = subject

    # Agregar el cuerpo del mensaje
    mensaje.attach(MIMEText(message_body, 'plain'))

    context = ssl.create_default_context()
    # Conectar al servidor SMTP y enviar el correo electrónico
    with smtplib.SMTP_SSL('mail.labaldosaflotante.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, mensaje.as_string())

    print('Correo electrónico enviado exitosamente')


def send_alert(db: Session, alert_id: int):
    alert = db.execute(select(User.name, User.email, Plant.name, Alert.title, Alert.notes, Alert.start_date, Alert.repeat, Alert.frecuency, Alert.status, AlertType.alert_name).where(
        User.id == Plant.owner_id, Plant.id == Alert.plant_id, Alert.alert_type_id == AlertType.id, Alert.id == alert_id)).first()
    username = alert[0]
    receiver = alert[1]
    plant_name = alert[2]
    alert_title = alert[3]
    alert_notes = alert[4]
    alert_start_date = alert[5]
    alert_repeat = alert[6]
    alert_frecuency = alert[7]
    alert_status = alert[8]
    alert_typename = alert[9]

    email_alert_subject = "Alerta de " + alert_typename + " para " + plant_name

    email_alert_text_repeat = "Es una alerta periódica, con frecuencia de " + str(alert_frecuency) + " días." +\
        "El próximo aviso será el " + str(alert_start_date) + "."

    email_alert_message = "Hola " + username + ",\n\n" + "Tienes una alerta de " + \
        alert_typename + " para tu planta: " + plant_name + ",\n" + \
        alert_title + "\n" + alert_notes + "\n\n"

    if (alert_repeat == True):
        email_alert_message = email_alert_message + email_alert_text_repeat + "\n\n"
    email_alert_message = email_alert_message + "Saludos,\n" + "Garden App"
    send_email(receiver, email_alert_subject, email_alert_message)
