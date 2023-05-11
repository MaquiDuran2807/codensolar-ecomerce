from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from io import BytesIO
import os
from xhtml2pdf import pisa
from .models import Products


def generate_pdf(email,templete,data):
    product=[]
    print(data["products"],"esto es data=====================================================================================================")
    for i in data["products"]:
        producto= Products.objects.get(id=i["product_id"])
        productos={
            "id":producto.id,
            "name":producto.name,
            "imagen":producto.image.url,
            "price":producto.price,
            "amount":i["amount"],
            "total":producto.price*i["amount"]
        }
        product.append(productos)


    # Obtener la plantilla HTML
    template = get_template(templete)
    html = template.render({"productos":product})
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
