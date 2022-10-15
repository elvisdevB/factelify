from email.mime.text import MIMEText
import smtplib


EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = 'elvis.burgos@unl.edu.ec'

EMAIL_HOST_PASSWORD = '1104951460'

EMAIL_DESTINY = "elviscursosadd@gmail.com"

def send_mail():
    try:
        print("Holaaaaa...")
        mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
        print("Conectado.....")

        #Contruimos el mensaje
        mensaje = MIMEText(""" Este es el mensaje que voy a enviar """)
        mensaje['From'] = EMAIL_HOST_USER
        mensaje['To'] = EMAIL_DESTINY
        mensaje['Subject'] = "Tienes un nuevo correo"

        mailServer.sendmail(EMAIL_HOST_PASSWORD,
                            EMAIL_DESTINY,
                            mensaje.as_string())
        
        print("Correo enviado correctamente")
    except Exception as e:
        print(e)

send_mail()