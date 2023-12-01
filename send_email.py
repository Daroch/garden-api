import os
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
print(EMAIL_USERNAME)


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


send_email('daroch314@gmail.com', 'Prueba', 'Hola, esto es una prueba')
