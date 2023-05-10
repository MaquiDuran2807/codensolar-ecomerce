from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from io import BytesIO
import os
from xhtml2pdf import pisa



def generate_pdf(email,templete,data):
    # Obtener la plantilla HTML
    template = get_template(templete)
    html = template.render(data)
    # Crear un archivo PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # Adjuntar el archivo PDF a un correo electrónico y enviarlo
    email = EmailMessage(
        'Asunto del correo electrónico',
        'Cuerpo del correo electrónico',
        'migue2807.maqd@gmail.com',
        [email]
    )
    email.attach('archivo.pdf', result.getvalue(), 'application/pdf')
    email.send()
    return "PDF generado y enviado por correo electrónico."

   
  
