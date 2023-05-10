import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.encoders import encode_base64

def send_mail(recipient,title,body,file_urls):
  # Definir las credenciales
  sender = "migue2807@gmail.com"
  password = "Ibague2022"

  # Definir los detalles del destinatario
  

  # Crear el mensaje
  message = MIMEMultipart()
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = title

  # Agregar el cuerpo del mensaje
  message.attach(MIMEText(body, "plain"))

  attachment = MIMEApplication(file_urls.read(), _subtype="pdf")
  attachment.add_header('Content-Disposition', 'attachment', filename=file_urls.name)
  message.attach(attachment)
    

  # Inciar sesión en servidor SMTP de gmail
  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(sender, password)

  # Enviar correo
  txt = message.as_string()
  server.sendmail(sender, recipient, txt)
  server.quit()

  print("mail sended")
  
