from django.http import HttpResponse
from django.template.loader import get_template
from django.core.mail import EmailMessage
from io import BytesIO
import os
from xhtml2pdf import pisa
from .models import Products
from django.conf import settings


def generate_pdf(email,templete,data):
    product=[]
    print(data["products"],"esto es data=====================================================================================================")
    contador=0
    for i in data["products"]:
        producto= Products.objects.get(id=i["product_id"])
        print('{}{}'.format(" http://127.0.0.1:8000",producto.image),"esto es la imagen=====================================================================================================")
        productos={
            "id":producto.id,
            "name":producto.name,
            "imagen":producto.image,
            "price":producto.price,
            "amount":i["amount"],
            "total":producto.price*i["amount"],
            "consumo_h":data["consumptions"][contador]["consumption_hr"],
            "consumo_D":data["consumptions"][contador]["consumption_day"] ,
            "perdidas":data["consumptions"][contador]["loss_consumption"],
            "total_MP":data["consumptions"][contador]["total_consumption_day"],    
        }
        contador+=1
        product.append(productos)
        panel={
            "panel":data["panel_needed"]["name"],
            "panel_precio_u":data["panel_needed"]["price"],
            "amount":data["panel_needed"]["amount"],
            "panel_precio_t":data["panel_needed"]["price"]*data["panel_needed"]["amount"],
            "panel_potencia":data["panel_needed"]["production"] ["production_hr"],
            "panel_potencia_dia":data["panel_needed"]["production"]["production_day"] ,
        }
        bateria={
            "bateria":data["battery_needed"]["name"],
            "bateria_precio_u":data["battery_needed"]["price"],
            "amount":data["battery_needed"]["amount"],
            "bateria_precio_t":data["battery_needed"]["price"]*data["battery_needed"]["amount"],
            "bateria_capacidad":data["battery_needed"]["capacity"] ,
            "bateria_capacidad_t":data["battery_needed"]["capacity"]*data["battery_needed"]["amount"]*12 ,
        }


    # Obtener la plantilla HTML
    template = get_template(templete)
    html = template.render({"productos":product,"p":panel,"b":bateria})
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
