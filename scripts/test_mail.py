from app import create_app, mail
from flask_mail import Message
import os
from dotenv import load_dotenv

load_dotenv()

app = create_app()

with app.app_context():
    print(f"Probando envío de email a: {os.getenv('ADMIN_EMAIL')}")
    print(f"Servidor: {app.config['MAIL_SERVER']}")
    print(f"Puerto: {app.config['MAIL_PORT']}")
    print(f"Usuario: {app.config['MAIL_USERNAME']}")
    
    msg = Message('Prueba de Conexión - Shavua BeShavua',
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[os.getenv('ADMIN_EMAIL')])
    msg.body = "Esta es una prueba de configuración de correo."
    
    try:
        mail.send(msg)
        print("¡Email enviado con éxito!")
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
